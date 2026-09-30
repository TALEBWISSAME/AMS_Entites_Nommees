#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

struct Codepoint {
    uint32_t value;
    std::size_t begin;
    std::size_t end;
};

struct RomanStats {
    std::string name;
    std::size_t pages = 0;
    std::size_t boundaries = 0;
    std::size_t tokens = 0;
    std::size_t candidates[4] = {0, 0, 0, 0};
};

struct CandidateKey {
    int n;
    std::string form;

    bool operator<(const CandidateKey& other) const {
        if (n != other.n) return n < other.n;
        return form < other.form;
    }
};

std::string read_file(const std::string& path) {
    std::ifstream in(path.c_str(), std::ios::binary);
    if (!in) throw std::runtime_error("lecture impossible: " + path);
    std::ostringstream buffer;
    buffer << in.rdbuf();
    return buffer.str();
}

void write_file(const std::string& path, const std::string& content) {
    std::ofstream out(path.c_str(), std::ios::binary);
    if (!out) throw std::runtime_error("ecriture impossible: " + path);
    out << content;
}

bool decode_utf8(const std::string& text, std::vector<Codepoint>& out) {
    out.clear();
    for (std::size_t i = 0; i < text.size();) {
        unsigned char c = static_cast<unsigned char>(text[i]);
        uint32_t value = 0;
        std::size_t length = 0;
        if (c <= 0x7F) {
            value = c;
            length = 1;
        } else if ((c & 0xE0) == 0xC0) {
            value = c & 0x1F;
            length = 2;
        } else if ((c & 0xF0) == 0xE0) {
            value = c & 0x0F;
            length = 3;
        } else if ((c & 0xF8) == 0xF0) {
            value = c & 0x07;
            length = 4;
        } else {
            return false;
        }
        if (i + length > text.size()) return false;
        for (std::size_t j = 1; j < length; ++j) {
            unsigned char cc = static_cast<unsigned char>(text[i + j]);
            if ((cc & 0xC0) != 0x80) return false;
            value = (value << 6) | (cc & 0x3F);
        }
        if ((length == 2 && value < 0x80) ||
            (length == 3 && value < 0x800) ||
            (length == 4 && value < 0x10000) ||
            value > 0x10FFFF ||
            (value >= 0xD800 && value <= 0xDFFF)) {
            return false;
        }
        out.push_back(Codepoint{value, i, i + length});
        i += length;
    }
    return true;
}

bool is_ascii_digit(uint32_t cp) {
    return cp >= '0' && cp <= '9';
}

bool is_letter(uint32_t cp) {
    if ((cp >= 'A' && cp <= 'Z') || (cp >= 'a' && cp <= 'z')) return true;
    if ((cp >= 0x00C0 && cp <= 0x00D6) || (cp >= 0x00D8 && cp <= 0x00F6) ||
        (cp >= 0x00F8 && cp <= 0x00FF)) return true;
    return cp == 0x0152 || cp == 0x0153 || cp == 0x0178;
}

bool is_token_core(uint32_t cp) {
    return is_letter(cp) || is_ascii_digit(cp);
}

bool is_uppercase_letter(uint32_t cp) {
    if (cp >= 'A' && cp <= 'Z') return true;
    if ((cp >= 0x00C0 && cp <= 0x00D6) || (cp >= 0x00D8 && cp <= 0x00DE)) return true;
    return cp == 0x0152 || cp == 0x0178;
}

bool is_apostrophe(uint32_t cp) {
    return cp == 0x0027 || cp == 0x2019;
}

bool is_hyphen(uint32_t cp) {
    return cp == 0x002D || (cp >= 0x2010 && cp <= 0x2014);
}

std::vector<std::string> tokenize_page(const std::string& page) {
    std::vector<Codepoint> cps;
    if (!decode_utf8(page, cps)) throw std::runtime_error("UTF-8 invalide dans une page");
    std::vector<std::string> tokens;
    std::size_t i = 0;
    while (i < cps.size()) {
        if (!is_token_core(cps[i].value)) {
            ++i;
            continue;
        }
        std::size_t start_byte = cps[i].begin;
        std::size_t last_core = i;
        ++i;
        while (i < cps.size()) {
            if (is_token_core(cps[i].value)) {
                last_core = i;
                ++i;
                continue;
            }
            if ((is_apostrophe(cps[i].value) || is_hyphen(cps[i].value)) &&
                i > 0 && i + 1 < cps.size() &&
                is_token_core(cps[i - 1].value) &&
                is_token_core(cps[i + 1].value)) {
                ++i;
                continue;
            }
            break;
        }
        tokens.push_back(page.substr(start_byte, cps[last_core].end - start_byte));
    }
    return tokens;
}

bool starts_with_uppercase(const std::string& token) {
    std::vector<Codepoint> cps;
    if (!decode_utf8(token, cps) || cps.empty()) return false;
    return is_uppercase_letter(cps.front().value);
}

std::vector<std::string> split_pages(const std::string& text, std::size_t& boundaries) {
    std::vector<std::string> pages;
    std::size_t start = 0;
    boundaries = 0;
    for (std::size_t i = 0; i < text.size(); ++i) {
        if (text[i] == '\f') {
            pages.push_back(text.substr(start, i - start));
            start = i + 1;
            ++boundaries;
        }
    }
    pages.push_back(text.substr(start));
    return pages;
}

std::string join_ngram(const std::vector<std::string>& tokens, std::size_t start, int n) {
    std::string out = tokens[start];
    for (int i = 1; i < n; ++i) {
        out += " ";
        out += tokens[start + i];
    }
    return out;
}

void process_roman(const std::string& name, const std::string& path,
                   std::map<CandidateKey, std::size_t>& frequencies,
                   RomanStats& stats) {
    stats.name = name;
    std::string text = read_file(path);
    std::vector<Codepoint> all_cps;
    if (!decode_utf8(text, all_cps)) throw std::runtime_error("UTF-8 invalide: " + path);
    std::size_t boundaries = 0;
    std::vector<std::string> pages = split_pages(text, boundaries);
    stats.pages = pages.size();
    stats.boundaries = boundaries;

    for (const std::string& page : pages) {
        std::vector<std::string> tokens = tokenize_page(page);
        stats.tokens += tokens.size();
        for (std::size_t i = 0; i < tokens.size(); ++i) {
            if (!starts_with_uppercase(tokens[i])) continue;
            for (int n = 1; n <= 3; ++n) {
                if (i + static_cast<std::size_t>(n) > tokens.size()) continue;
                std::string form = join_ngram(tokens, i, n);
                if (form.empty()) continue;
                ++frequencies[CandidateKey{n, form}];
                ++stats.candidates[n];
            }
        }
    }
}

std::string basename_without_extension(const std::string& filename) {
    std::size_t slash = filename.find_last_of("/\\");
    std::string base = slash == std::string::npos ? filename : filename.substr(slash + 1);
    std::size_t dot = base.find_last_of('.');
    return dot == std::string::npos ? base : base.substr(0, dot);
}

int main(int argc, char** argv) {
    try {
        if (argc < 4) {
            std::cerr << "Usage: generate_l OUTPUT_LIST OUTPUT_STATS INPUT...\n";
            return 2;
        }
        std::string output_list = argv[1];
        std::string output_stats = argv[2];
        std::map<CandidateKey, std::size_t> frequencies;
        std::vector<RomanStats> roman_stats;

        for (int i = 3; i < argc; ++i) {
            RomanStats stats;
            process_roman(basename_without_extension(argv[i]), argv[i], frequencies, stats);
            roman_stats.push_back(stats);
        }

        std::ostringstream list;
        list << "n\tforme\tfrequence\n";
        for (const auto& item : frequencies) {
            list << item.first.n << '\t' << item.first.form << '\t' << item.second << '\n';
        }
        write_file(output_list, list.str());

        std::size_t total_tokens = 0;
        std::size_t total_pages = 0;
        std::size_t total_boundaries = 0;
        std::size_t total_candidates[4] = {0, 0, 0, 0};
        std::size_t unique_by_n[4] = {0, 0, 0, 0};
        for (const auto& item : frequencies) ++unique_by_n[item.first.n];

        std::ostringstream stats;
        stats << "Génération de L\n";
        stats << "Format liste: n<TAB>forme<TAB>frequence\n";
        stats << "Critère: n-grammes n=1,2,3 dont le premier token commence par une majuscule\n";
        stats << "Frontière U+000C: aucune séquence ne traverse une page\n\n";
        stats << "roman\ttokens\tpages\tfrontieres\tcandidats_n1\tcandidats_n2\tcandidats_n3\n";
        for (const RomanStats& row : roman_stats) {
            stats << row.name << '\t' << row.tokens << '\t' << row.pages << '\t'
                  << row.boundaries << '\t' << row.candidates[1] << '\t'
                  << row.candidates[2] << '\t' << row.candidates[3] << '\n';
            total_tokens += row.tokens;
            total_pages += row.pages;
            total_boundaries += row.boundaries;
            for (int n = 1; n <= 3; ++n) total_candidates[n] += row.candidates[n];
        }
        stats << "TOTAL\t" << total_tokens << '\t' << total_pages << '\t'
              << total_boundaries << '\t' << total_candidates[1] << '\t'
              << total_candidates[2] << '\t' << total_candidates[3] << "\n\n";
        stats << "formes_uniques_n1=" << unique_by_n[1] << '\n';
        stats << "formes_uniques_n2=" << unique_by_n[2] << '\n';
        stats << "formes_uniques_n3=" << unique_by_n[3] << '\n';
        stats << "formes_uniques_total=" << frequencies.size() << '\n';
        stats << "occurrences_candidates_total="
              << (total_candidates[1] + total_candidates[2] + total_candidates[3]) << '\n';
        stats << "traversees_u000c=0\n";
        write_file(output_stats, stats.str());

        std::cout << stats.str();
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Erreur: " << error.what() << '\n';
        return 1;
    }
}

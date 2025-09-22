#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

enum class TokenType
{
    KEYWORD,
    IDENTIFIER,
    INTEGER_LITERAL,
    FLOAT_LITERAL,
    OPERATOR,
    PUNCTUATOR,
    UNKNOWN
};

struct Token
{
    TokenType type;
    string value;
    Token(TokenType t, const string &v) : type(t), value(v) {}
};

class LexicalAnalyzer
{
private:
    string input;
    size_t position;
    unordered_map<string, TokenType> keywords;
    void initKeywords()
    {
        for (string k : {"int", "float", "if", "else", "while", "return"})
            keywords[k] = TokenType::KEYWORD;
    }
    bool isWhitespace(char c) { return c == ' ' || c == '\t' || c == '\n' || c == '\r'; }
    bool isAlpha(char c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'); }
    bool isDigit(char c) { return c >= '0' && c <= '9'; }
    bool isAlphaNumeric(char c) { return isAlpha(c) || isDigit(c); }
    string getNextWord()
    {
        size_t s = position;
        while (position < input.size() && isAlphaNumeric(input[position]))
            position++;
        return input.substr(s, position - s);
    }
    string getNextNumber()
    {
        size_t s = position;
        bool d = false;
        while (position < input.size() && (isDigit(input[position]) || input[position] == '.'))
        {
            if (input[position] == '.')
            {
                if (d)
                    break;
                d = true;
            }
            position++;
        }
        return input.substr(s, position - s);
    }

public:
    LexicalAnalyzer(const string &src) : input(src), position(0) { initKeywords(); }
    vector<Token> tokenize()
    {
        vector<Token> tokens;
        while (position < input.size())
        {
            char c = input[position];
            if (isWhitespace(c))
            {
                position++;
                continue;
            }
            if (isAlpha(c))
            {
                string w = getNextWord();
                tokens.emplace_back(keywords.count(w) ? TokenType::KEYWORD : TokenType::IDENTIFIER, w);
            }
            else if (isDigit(c))
            {
                string n = getNextNumber();
                tokens.emplace_back(n.find('.') != string::npos ? TokenType::FLOAT_LITERAL : TokenType::INTEGER_LITERAL, n);
            }
            else if (c == '+' || c == '-' || c == '*' || c == '/')
            {
                tokens.emplace_back(TokenType::OPERATOR, string(1, c));
                position++;
            }
            else if (c == '(' || c == ')' || c == '{' || c == '}' || c == ';')
            {
                tokens.emplace_back(TokenType::PUNCTUATOR, string(1, c));
                position++;
            }
            else
            {
                tokens.emplace_back(TokenType::UNKNOWN, string(1, c));
                position++;
            }
        }
        return tokens;
    }
};

string getTokenTypeName(TokenType t)
{
    switch (t)
    {
    case TokenType::KEYWORD:
        return "KEYWORD";
    case TokenType::IDENTIFIER:
        return "IDENTIFIER";
    case TokenType::INTEGER_LITERAL:
        return "INTEGER_LITERAL";
    case TokenType::FLOAT_LITERAL:
        return "FLOAT_LITERAL";
    case TokenType::OPERATOR:
        return "OPERATOR";
    case TokenType::PUNCTUATOR:
        return "PUNCTUATOR";
    case TokenType::UNKNOWN:
        return "UNKNOWN";
    default:
        return "UNDEFINED";
    }
}

void printTokens(const vector<Token> &tokens)
{
    for (auto &t : tokens)
        cout << "Type: " << getTokenTypeName(t.type) << ", Value: " << t.value << endl;
}

int main()
{
    string src = "int main() { float x=3.14; float y=3.15; float z=x+y; return 0; }";
    LexicalAnalyzer lexer(src);
    auto tokens = lexer.tokenize();
    cout << "Source code: " << src << "\n\nTokens Generate by Lexical Analyzer:\n";
    printTokens(tokens);
}

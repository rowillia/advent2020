use lazy_static::lazy_static;
use regex::Regex;
use std::io;
use std::io::BufRead;

lazy_static! {
    static ref PASSWORD_LINE_RE: Regex =
        Regex::new(r"(?P<first>\d+)\-(?P<second>\d+)\s+(?P<letter>\w):\s+(?P<password>\w+)")
            .unwrap();
}

#[derive(Debug, PartialEq)]
struct PasswordLine {
    first: u32,
    second: u32,
    letter: char,
    password: String,
}

fn parse_line(line: &str) -> Option<PasswordLine> {
    match PASSWORD_LINE_RE.captures(line) {
        Some(n) => Some(PasswordLine {
            first: n["first"].parse::<u32>().ok()?,
            second: n["second"].parse::<u32>().ok()?,
            letter: n["letter"].chars().next()?,
            password: n["password"].to_string(),
        }),
        None => None,
    }
}

fn is_line_valid_part1(line: &str) -> bool {
    match parse_line(line) {
        Some(n) => (n.first..n.second + 1).contains(&(n.password.matches(n.letter).count() as u32)),
        None => false,
    }
}

fn nth_password_char(password_line: &PasswordLine, n: u32) -> char {
    password_line
        .password
        .chars()
        .nth((n - 1) as usize)
        .unwrap_or('\0')
}

fn is_line_valid_part2(line: &str) -> bool {
    match parse_line(line) {
        Some(n) => {
            let first_char = nth_password_char(&n, n.first);
            let second_char = nth_password_char(&n, n.second);
            (first_char == n.letter) ^ (second_char == n.letter)
        }
        None => false,
    }
}

fn main() {
    let stdin = io::stdin();
    let result = stdin
        .lock()
        .lines()
        .map(|l| l.unwrap_or_else(|_| "".to_string()))
        .map(|l| (is_line_valid_part1(&l), is_line_valid_part2(&l)))
        .fold((0, 0), |acc, x| {
            (acc.0 + (x.0 as u32), acc.1 + (x.1 as u32))
        });
    println!("part1: {}, part2: {}", result.0, result.1)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_line() -> Result<(), String> {
        assert_eq!(
            parse_line("1-3 a: abcde"),
            Some(PasswordLine {
                first: 1,
                second: 3,
                letter: 'a',
                password: "abcde".to_string(),
            })
        );
        assert_eq!(
            parse_line("32-44 a: abcde"),
            Some(PasswordLine {
                first: 32,
                second: 44,
                letter: 'a',
                password: "abcde".to_string(),
            })
        );
        assert_eq!(parse_line("hello-44 a: abcde"), None);
        assert_eq!(parse_line("32-world a: abcde"), None);
        Ok(())
    }

    #[test]
    fn test_is_line_valid_part1() -> Result<(), String> {
        assert_eq!(is_line_valid_part1("1-3 a: abcde"), true);
        assert_eq!(is_line_valid_part1("1-3 a: abcdeaa"), true);
        assert_eq!(is_line_valid_part1("1-3 a: bcde"), false);
        assert_eq!(is_line_valid_part1("1-3 a: abcdeaaa"), false);
        Ok(())
    }

    #[test]
    fn test_is_line_valid_part2() -> Result<(), String> {
        assert_eq!(is_line_valid_part2("1-3 a: abcde"), true);
        assert_eq!(is_line_valid_part2("1-3 a: cbade"), true);
        assert_eq!(is_line_valid_part2("1-3 a: abade"), false);
        assert_eq!(is_line_valid_part2("1-3 a: cbgb"), false);
        Ok(())
    }
}

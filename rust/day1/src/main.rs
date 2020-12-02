use std::collections::HashSet;
use std::env;
use std::io;
use std::io::BufRead;

fn two_sum(values: impl Iterator<Item=i32>, target: i32) -> Option<(i32, i32)>
{
    let mut values_as_set = HashSet::<i32>::new();
    for value in values {
        if values_as_set.contains(&(target - value)) {
            return Some((value, target - value));
        } else {
            values_as_set.insert(value);
        }
    }
    return None;
}

fn three_sum<'a>(values: Vec<i32>, target: i32) -> Option<(i32, i32, i32)>
{
    for (i, value) in values.iter().enumerate() {
        match two_sum(values.iter().enumerate().filter(|&(j, _)| i != j).map(|(_, v)| *v), target - value) {
            Some(n) => return Some((n.0, n.1, *value)),
            None => ()
        }
    }
    return None;
}

fn main() {
    let stdin = io::stdin();
    let input = stdin.lock().lines().map(|l| l.unwrap().parse::<i32>().unwrap());
    let args: Vec<String> = env::args().collect();
    if args.len() == 2 && args[1] == "-3" {
        match three_sum(input.collect(), 2020) {
            Some(n) => println!("{:?}", n.0 * n.1 * n.2),
            None => ()
        }
    } else {
        match two_sum(input, 2020) {
            Some(n) => println!("{:?}", n.0 * n.1),
            None => ()
        } 
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_two_sum() -> Result<(), String> {
        assert_eq!(two_sum([1, 2, 3].iter().cloned(), 4), Some((3, 1)));
        assert_eq!(two_sum([1, 2, 3].iter().cloned(), 42), None);
        assert_eq!(two_sum([1, 2, 3].iter().cloned(), 6), None);
        Ok(())
    }
    
    #[test]
    fn test_three_sum() -> Result<(), String> {
        assert_eq!(three_sum(vec![1, 2, 3], 4), None);
        assert_eq!(three_sum(vec![1, 2, 3], 42), None);
        assert_eq!(three_sum(vec![1, 2, 3], 6), Some((3, 2, 1)));
        Ok(())
    }
}
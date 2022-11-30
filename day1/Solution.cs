using System;

string[] INPUT = File.ReadAllLines("./input.txt");

string Part1(string[] INPUT)
{
    return string.Join(" ", INPUT);
}

string Part2(string[] INPUT)
{
    return string.Concat(INPUT);
}

Console.WriteLine(Part1(INPUT));
Console.WriteLine(Part2(INPUT));

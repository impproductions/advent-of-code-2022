using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
class Program
{
    static void Main()
    {
        string input = File.ReadAllText("./input.txt");
        string[] data = input.Split("\n\n");

        List<int> GetCaloriesList(string[] input)
        {
            List<int> caloriesList = input.Select(v => v.Split("\n").Select(c => int.Parse(c)).Sum()).ToList();
            caloriesList.Sort((a, b) => b-a);

            return caloriesList;
        }

        int Part1(string[] input)
        {
            return GetCaloriesList(input)[0];
        }

        int Part2(string[] input)
        {
            List<int> caloriesList = GetCaloriesList(input);
            return caloriesList.GetRange(0, 3).Sum();
        }

        Console.WriteLine(Part1(data));
        Console.WriteLine(Part2(data));
    }
}


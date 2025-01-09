// #r "System.Console"
// Console.Out.WriteLine("This is the miracle");
Console.WriteLine("enter val");
int val = int.Parse(Console.ReadLine());
int res = func(val);
Console.WriteLine($"result: {res}");

int func(int val) {
    if(val <= 1) {
        Console.WriteLine("0 ");
        return val;
    }
    int a = 0;
    int b = 1;
    for(int i = 0; i <= val; i++){
        int tmp = a + b;
        b = a;
        a = tmp;
        Console.WriteLine($"{a} ");
    }
    return a;
}

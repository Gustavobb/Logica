{
    bool a;
    int b;
    string c;

    a = true;
    b = 1;

    while(a)
    {
        b = b + 1;
        if (b > 10) a = false;
    }

    c = "test";

    println(c);
    println(b);
    println(a);
}
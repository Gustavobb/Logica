int soma(int x, int y) {
    int r;
    r = x + y;
    
    if (r < 100)
        r = 10;
    
    return r;
}

int main() {
    int a;
    int b;
    a = 3;
    b = soma(a, 4);
    println(a);
    println(b);
}
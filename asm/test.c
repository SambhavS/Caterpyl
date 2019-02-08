int main(){
    int N = 10;
    int temp = 0;
    int f1 = 0;
    int f2 = 1;
    while(N > 0){
        temp = f1;
        f1 = f2;
        f2 = f1 + temp;
        N -= 1;
    }
    return f1;
}
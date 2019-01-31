int main(){
    int nthNum = 15;
    int x = 0;
    int y = 1;
    int temp = 0;
    int c = 0;
    while (c < nthNum){
        temp = x;
        x = y;
        y = temp + y;
        c = c + 1;
    }
    return x;
}
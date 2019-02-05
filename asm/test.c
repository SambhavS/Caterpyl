int main(){
    return fact(10, 20);
}
int fact(int x, int y){
    if(x == 1){
        return 1 + y;
    }
    return x * fact(x-1, y);
}
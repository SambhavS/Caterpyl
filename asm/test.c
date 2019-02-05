int main(){
    return foo();
}
int foo(){
    return max(1, 2);
}
int max(int a, int b){
    if(a >b ){
        return a;
    }
    return b;
}
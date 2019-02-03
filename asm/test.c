int main(){
    int a = foo();
    int z = foo();
    return a*z;
}
int foo(){
    int b = 2;
    int c = 3;
    return b * c;
}
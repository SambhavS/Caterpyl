int main(){
    return foo(33);
}

int foo(int x){
    return bar(x, 1, 4);
}

int bar(int x, int y, int z){
    return zoo(x, y+z);
}

int zoo(int x, int y){
    return 77;
}

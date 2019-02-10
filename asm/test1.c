int main(){
    int x = 0;
    bool done = False;
    while(!done){
        x += 10;
        if(x>100){
            done = True;
        }
    }
    return x;
}
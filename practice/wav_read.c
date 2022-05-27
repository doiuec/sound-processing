#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define  MEM_SIZE 16000  

int main(int argc, char **argv){

    FILE *f1;
    int size, ch, sample_rate;

//TODO:入力引数の検査
    if( argc != 2){
        fprintf( stderr, "Usage: .exe input.wav\n");
        exit(1);
    }

//TODO:ファイルを開く
    f1 = fopen( argv[1], "rb");
    if(f1 == NULL){
        printf("failed to open\n");
        exit(1);
    }

//TODO:ファイル情報の取得
    printf("========== wav inf ==========\n");
    fseek(f1, 4, SEEK_SET);
    fread(&size, 4, 1, f1);
    fseek(f1, 22, SEEK_SET);
    fread(&ch, 2, 1, f1);
    fseek(f1, 24, SEEK_SET);
    fread(&sample_rate, 4, 1, f1);
    printf("size       = %d bytes\n",  size);
    printf("ch         = %d ch\n",  ch);
    printf("sample rate= %d \n",  sample_rate);

    fclose(f1);
    return 0;
}

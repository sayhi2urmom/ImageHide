#include <stdio.h>
#include <opencv2/opencv.hpp>
#include<bitset>
#include<stdlib.h>

using namespace cv;
int main(int argc, char** argv )
{
    if ( argc != 3 )
    {
        printf("usage: main path_to_img length\n");
        return -1;
    }
    int length=atoi(argv[2]);

    Mat image;
    std::vector<cv::Mat> rgbChannels(3);
    image = imread( argv[1], 1 );
    if ( !image.data )
    {
        printf("No image data \n");
        return -1;
    }


    split(image, rgbChannels);

    int rows = image.rows;
    int cols = image.cols;
    int num_el = rows*cols;
    
    Mat flatten;
    flatten=image.reshape(1,num_el);
    
    std::bitset<8> temp;
    unsigned char* s=(unsigned char*)(new char[int(length/8)]);

    for(int i=1;i<=length;i++){
        int lsb= int(flatten.at<Vec3b>(i-1,0)[0]) % 2 ;
        //std::cout << lsb ;
        temp.set(7-((i-1)%8),lsb);
        if(i%8==0){
            
            s[int(i/8)-1]=(unsigned char)temp.to_ulong();
            temp.reset();
        }

    }
    for(int ii=0;ii<int(length/8);ii++){
        putchar(s[ii]);
    }

    return 0;
}

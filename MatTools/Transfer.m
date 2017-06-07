clear;
clc;
fid = fopen('list.txt');
tline = fgetl(fid);
count = 0;

count = count + 1;
img = imread(tline);
img2 = TransImage_3brand(img);
dir = ['imgetif8\' tline(32:length(tline) - 3) 'tif'];
imwrite(img2, dir);

while ischar(tline)
    disp(tline)
    tline = fgetl(fid);
    count = count + 1;
    img = imread(tline);
    img2 = TransImage_3brand(img);
    dir = ['imgetif8\' tline(32:length(tline) - 3) 'tif'];
    imwrite(img2, dir);
    %subdir = ['imge8\' tline(32:length(tline) - 4) ];
    %mkdir subdir;
    %[m n z] = size(img2);
    %stride_m = uint16(m/4);
    %stride_n = uint16(n/4);
    %for i = 1:4
    
    %end
end
fclose(fid);
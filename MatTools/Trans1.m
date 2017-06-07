img = imread('14SEP09105708-S3DS_R1C1-053971692010_01_P001.tif');
img2 = TransImage_3brand(img);
name = '14SEP09105708-S3DS_R1C1-053971692010_01_P001.tif';
[m n z] = size(img2);
    for j = 1: 3%±íÊ¾ĞĞ
        for k = 1:3
            subimg = img2((j - 1)*4000 + 1:j*4000,(k - 1)*4000 + 1:k*4000,:);
            
            subname = ['subimg\' name(1:length(name) - 4) '_' num2str(j) '_' num2str(k) '.tif'];
            imwrite(subimg, subname);
        end
    end
    for j = 4
        for k = 1:3
            subimg = img2((j - 1)*4000 + 1:m, (k - 1)*4000 + 1:k*4000,:);
            subname = ['subimg\' name(1:length(name) - 4) '_' num2str(j) '_' num2str(k) '.tif'];
            imwrite(subimg, subname);
        end
    end
    for j = 1:3
        for k = 4
            subimg = img2((j - 1)*4000 + 1:j*4000, (k - 1)*4000 + 1:n,:);
            subname = ['subimg\' name(1:length(name) - 4) '_' num2str(j) '_' num2str(k) '.tif'];
            imwrite(subimg, subname);
        end
    end
    j = 4;
    k = 4;
    subimg = img2((j - 1)*4000 + 1:m, (k - 1)*4000 + 1:n,:);
    subname = ['subimg\' name(1:length(name) - 4) '_' num2str(j) '_' num2str(k) '.jpg'];
    imwrite(subimg, subname); 

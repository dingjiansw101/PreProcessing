fileFolder=fullfile('.');
suffix = '*.tiff'
dirOutput=dir(fullfile(fileFolder, suffix));
fileNames={dirOutput.name}';

for i = 1:length(fileNames)
    name = fileNames(i);
    name = name{1};
    %img = imread(name);
    img2 = TransImg(name);
    %dir = ['img8\' name];
    %imwrite(img2, dir);
    splitgray(img2, name, 4000, 0);
end

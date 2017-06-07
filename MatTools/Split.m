fileFolder=fullfile('.');
dirOutput=dir(fullfile(fileFolder,'*.tif'));
fileNames={dirOutput.name}';

for i = 1:length(fileNames)
    name = fileNames(i);
    name = name{1};
    img = imread(name);
    %dir = ['img8\' name];
    %imwrite(img2, dir);
    splitgray(img, name, 4000, 0);
end

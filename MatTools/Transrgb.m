function [ output ] = TransImage_3brand( input )
%Tansfer the 16 bit image to 8 bit image
%   Detailed explanation goes here
    %[m n] = size(input);
    upborder_1 = max(max(input(:,:,1)));
    downborder_1 = min(min(input(:,:,1)));
    upborder_2 = max(max(input(:,:,2)));
    downborder_2 = min(min(input(:,:,2)));
    upborder_3 = max(max(input(:,:,3)));
    downborder_3 = min(min(input(:,:,3)));
    output = zeros(size(input));
    output(:,:,1) = (double(input(:,:,1)) - double(downborder_1))*255/(double(upborder_1) - double(downborder_1));
    output(:,:,2) = (double(input(:,:,2)) - double(downborder_2))*255/(double(upborder_2) - double(downborder_2));
    output(:,:,3) = (double(input(:,:,3)) - double(downborder_3))*255/(double(upborder_3) - double(downborder_3));
    %output = (double(input) - double(downborder))*255/(double(upborder) - double(downborder));
    output = uint8(output);
end
function splitgray(img, name, len, overlap)
[m n z] = size(img);
%img2 = TransImage_3brand(img);

[path, filename, suffix] = fileparts(name)
suffixlen = length(suffix)
p = fix(n/len);
w = mod(n, len);
half = len/2;
if w <= half
    n_stride = p;
else
    n_stride = p+1;
end

p = fix(m/len);
w = mod(m, len);
if w <= half
    m_stride = p;
else
    m_stride = p+1;
end
for j = 1:m_stride-1
    for k = 1:n_stride-1
            subimg = img((j - 1)*(len-overlap) + 1:j*(len-overlap),(k - 1)*(len - overlap) + 1:k*(len - overlap));
            subname = ['subimg\' name(1:length(name) - suffixlen) '_' num2str(j) '_' num2str(k) '.tiff'];
            imwrite(subimg, subname);
    end
end
    for j = m_stride
        for k = 1:n_stride-1
            subimg = img((j - 1)*(len - overlap) + 1:m, (k - 1)*(len - overlap) + 1:k*(len - overlap));
            subname = ['subimg\' name(1:length(name) - suffixlen) '_' num2str(j) '_' num2str(k) '.tiff'];
            imwrite(subimg, subname);
        end
    end
    for j = 1:m_stride - 1
        for k = n_stride
            subimg = img((j - 1)*(len - overlap) + 1:j*(len - overlap), (k - 1)*(len - overlap) + 1:n);
            subname = ['subimg\' name(1:length(name) - suffixlen) '_' num2str(j) '_' num2str(k) '.tiff'];
            imwrite(subimg, subname);
        end
    end
    j = m_stride;
    k = n_stride;
    subimg = img((j - 1)*(len - overlap) + 1:m, (k - 1)*(len - overlap) + 1:n);
    subname = ['subimg\' name(1:length(name) - suffixlen) '_' num2str(j) '_' num2str(k) '.tiff'];
    imwrite(subimg, subname); 
end
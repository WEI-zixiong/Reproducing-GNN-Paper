%% write txt files
% 1-load node_features first
% manually
% 2-conversion
test=table2array(nodefeatures);
% 3-convert to cell

%% write data file
test=table2array(nodefeatures);
num =1;
for i = 1:3:1200
    data{num} = test(i:i+2,:);
    num = num+1;
end
for i = 1:400
    % remove nan
    for j = 1:3
        data_no_NaN{i}(j,:) = rmmissing(data{i}(j,:)); 
    end
    % tranverse the matrix
    data_no_NaN_trans{i}=data_no_NaN{i}';
    % find box min/max
    for j = 1:3
        MAX(i,j)=max(data_no_NaN_trans{i}(:,j));
        MIN(i,j)=min(data_no_NaN_trans{i}(:,j));
    end
    % add atome-ID atome-type
    row = size(data_no_NaN_trans{i},1); 
    data_final{i}(1:row,1) = [1:1:row];
    data_final{i}(1:row,2) = ones(row,1);
    data_final{i}(:,3:5) = data_no_NaN_trans{i};
    % write initial part of data file
    filename = ['structure',num2str(i),'.data'];
    fid=fopen(filename,'w');
    fprintf(fid,'lammps data\n');
    fprintf(fid,'\n');
    fprintf(fid,'%d atoms \n',size(data_no_NaN_trans{i},1));
    fprintf(fid,'\n');
    fprintf(fid,'%d atom types \n',1);
    fprintf(fid,'\n');
    fprintf(fid,'#simulation box \n');
    fprintf(fid,'%f %f xlo xhi\n',MIN(i,1)-1, MAX(i,1)+1); 
    fprintf(fid,'%f %f ylo yhi\n',MIN(i,2)-1, MAX(i,2)+1);
    fprintf(fid,'%f %f zlo zhi\n',MIN(i,3)-1, MAX(i,3)+1);
    fprintf(fid,'\n');
    fprintf(fid,'Masses\n');
    fprintf(fid,'\n');
    fprintf(fid,'%d %f \n',1, 26.981539);
    fprintf(fid,'\n');
    fprintf(fid,'Atoms\n');
    fprintf(fid,'\n');
    % write coordinates
    for k = 1:size(data_no_NaN_trans{i},1)
        fprintf(fid,'%d %d %f %f %f \n',data_final{i}(k,1), data_final{i}(k,2), data_final{i}(k,3), data_final{i}(k,4), data_final{i}(k,5)); 
    end
    fclose(fid);
end

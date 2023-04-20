%% 图表分析
clear
clc
close
load positions.mat
All = [x_max; x_min; y_max; y_min];
names = ["x_{max}", "x_{min}", "y_{max}", "y_{min}"];
for k = 1:4
    subplot(4,1,k)
    if k <= 2
        m = 1280;
    else
        m = 640;
    end
    histogram(All(k, :), m/10)
    xlabel('pixels')
    ylabel('counts')
    xlim([0, m])
    xticks(0:20:m)
    set(gca, 'FontSize', 10)
    title(names(k), "FontSize", 15)
end

%% 计算外点概率（y）
span    = 150;
center  = 320;
y = [y_max, y_min];
k = find(y < (center-span) | y >= (center + span));
size(k, 2) / size(y, 2)

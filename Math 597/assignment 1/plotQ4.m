%errorClassSchedule = errorAverage;
errorMySchedule = errorAverage;  

x = 1:400;
y1=errorClassSchedule;
y2=errorMySchedule;

cla reset;
%ylabel('f(x_k)-f^*');
plot(x,y1,'DisplayName','Assignment Schedule')
hold on
plot(x,y2,'DisplayName','1\k Schedule')
title('f(x_k) - f^* (SGD - Average over 10 runs)')
xlabel('k') 
set(gca, 'YScale', 'log')


legend
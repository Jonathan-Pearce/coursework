A=[1,2;2,3]
N=20
n=10000

%create points on unit circle
angle = 2*pi/N;

u = zeros(2,N);

for i = 0:N
    %parition unit cirle
    u(1,i+1) = cos(angle*i);
    u(2,i+1) = sin(angle*i);
end

%ellipse points
e = A*u;
%random unit cirle points
points = randn(2,n);
%random ellipse points
transPoints = A*points;

figure();
%scatter(u(1,:),u(2,:))
scatter(points(1,:),points(2,:),'r')
hold on
scatter(transPoints(1,:),transPoints(2,:),'b')
plot(u(1,:),u(2,:),'k')
plot(e(1,:),e(2,:),'k')
xlabel('e1-axis');
ylabel('e2-axis');
title('Geometry of Action of A on the Unit Circle and n Randomly Generated Points (n=10000)');
legend('Red dot = random points in the domain','Blue dot=image under action of A of the random points');
xlim([-10 10]);
ylim([-10 10]);
hold off;
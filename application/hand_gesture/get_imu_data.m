% From MobilePhone IOS MATLAB
% 1. Click on sensor page and start the sensor device

% From PC 
% 1. connector on <pwd>
% 2. `m = mobiledev`
% 3. enable sensor 
%    '''
%    m.AccelerationSensorEnabled    = 1
%	 m.AngularVelocitySensorEnabled = 1
%    m.MagneticSensorEnabled        = 1
%    m.OrientationSensorEnabled     = 1
%    m.PositionSensorEnabled        = 1
%    m.Logging = 1
%    '''
% Sleep func
% java.lang.Thread.sleep(duration*1000)  
%
% Author : tcyu@umich.edu
% Date   : 2019/01/18 

function get_imu_data(sensor, duration, file, frequency)

	sleep_t = 1/frequency
	sections = duration/sleep_t
	f = fopen(file, 'w')
	fprint('[INFO] Start recording ... %s', datetime('now'))
	for i = 1:sections
		[acc_x acc_y acc_z] = sensor.Acc
	    [yaw roll to]       = sensor.Ang
	    [A B C]             = sensor.Ori
	    data = sprintf('%f,%f,%f,%f,%f,%f,%f,%f,%f,%s\n', 
	            acc_x, acc_y, acc_z, yaw, roll, to, A, B, C)
        fprint(f, data)
        sleep(sleep_t)
    end
    fprint('[INFO] Complete! %s', datetime('now'))
end

function sleep(time)
	% in miliseconds
	java.lang.Thread.sleep(time)  
end

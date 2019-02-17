import time
def clamp(num,lower,upper):
	return lower if num < lower else upper if num > upper else num
	
class PID:
	def __init__(self):
		self.started = False
		self.kp = 0
		self.kd = 0
		self.ki = 0
		self.prev_error = 0
		self.prev_time = 0
		self.cum_error = 0
		self.prev_error_time = 0
	def set_gains(self,kp,ki,kd):
		self.kp = kp
		self.ki = ki
		self.kd = kd
	def step(self, error):
		t = time.time()
		if self.started:
			dt = t-self.prev_time
			d_error = (error-self.prev_error)/(t-self.prev_error_time)
			self.cum_error+=error*dt
			output = self.kp*error + self.ki*self.cum_error + self.kd*d_error
			self.prev_time = t
			if(t-self.prev_error_time > 20):
				self.prev_error_time = t
				self.prev_error = error
			return clamp(output,0,100)
		else:
			self.prev_time = t
			self.prev_error = error
			self.prev_error_time = t
			self.started=True
			return 0 
	def reset(self):
		self.cum_error = 0
		self.started = False
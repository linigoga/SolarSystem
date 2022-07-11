import numpy as np
from scipy.constants import gravitational_constant as G
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import animation


class Planet:
    def __init__(self,name : str, x : int, y: int, vx : float, vy : float,mass : float) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.positions_x = list([x])
        self.positions_y = list([y])
        self.vel_x = list([vx])
        self.vel_y = list([vy])
        pass
    
    def log_position(self,posx,posy,velx,vely) -> None:
        self.positions_x.append(posx)
        self.positions_y.append(posy)
        self.vel_x.append(velx)
        self.vel_y.append(vely)
        return

class Star:
    def __init__(self,x,y,mass) -> None:
        self.mass = mass
        self.x = x
        self.y = y


class System:
    def __init__(self,sun,planets : list) -> None:
        self.planets = planets
        self.sun = sun
        pass

    
    def calculate_gravitational_force(self,m,m1,r) -> float:
        """
        Calculate the gravitational force F = -G m1 m2 / r^3/2
        """

        return -G*m*m1/r

    def update_planet_positions(self):
        # The main interaction would be with the Sun since the mass of the sun is substantially bigger 
        # than any other planet. However, the other planets can still yield some influence between
        #every other planet's orbit.

        dt = 86400


        for p in self.planets:
            m = p.mass
            x = p.x; y = p.y
                
            
            
            x_del = x - self.sun.x;y_del = y - self.sun.y
            r = (x_del**2 + y_del**2 )**(3/2)


            F = self.calculate_gravitational_force(self.sun.mass,m,r)
                

            ax = F*x_del/m
            ay = F*y_del/m
            p.vx += ax*dt; p.vy += ay*dt
            p.x += p.vx*dt;p.y += p.vy*dt


            #update positions and log into the object
            p.log_position(p.x,p.y,p.vx,p.vy)
            


        return
    
    def animate_solar_system(self,time):
        AU = 1.5e11
        fig,ax = plt.subplots()
        ax.set_aspect('equal')
        ax.grid()


        lineM,    = ax.plot([],[],'-',lw='1')
        pointsM,  = ax.plot([self.planets[0].positions_x[0]],[0],marker='o',
                        markersize = 4)
        textsM   = ax.text(self.planets[0].positions_x[0],0,self.planets[0].name)

        lineV,    = ax.plot([],[],'-',lw='1')
        pointsV,  = ax.plot([self.planets[1].positions_x[0]],[0],marker='o',
                        markersize = 4)
        textsV   = ax.text(self.planets[1].positions_x[0],0,self.planets[1].name)

        lineE,    = ax.plot([],[],'-',lw='1')
        pointsE,  = ax.plot([self.planets[2].positions_x[0]],[0],marker='o',
                        markersize = 4)
        textsE   = ax.text(self.planets[2].positions_x[0],0,self.planets[2].name)


        lineMa,    = ax.plot([],[],'-',lw='1')
        pointsMa,  = ax.plot([self.planets[3].positions_x[0]],[0],marker='o',
                        markersize = 4)
        textsMa   = ax.text(self.planets[3].positions_x[0],0,self.planets[3].name)


        ax.set_xlim(-3*AU,3*AU)
        ax.set_ylim(-3*AU,3*AU)
        

        def update(i):

            lineM.set_data(self.planets[0].positions_x[:i],self.planets[0].positions_y[:i])
            pointsM.set_data(self.planets[0].positions_x[i],self.planets[0].positions_y[i])
            textsM.set_position((self.planets[0].positions_x[i],self.planets[0].positions_y[i]))

            lineV.set_data(self.planets[1].positions_x[:i],self.planets[1].positions_y[:i])
            pointsV.set_data(self.planets[1].positions_x[i],self.planets[1].positions_y[i])
            textsV.set_position((self.planets[1].positions_x[i],self.planets[1].positions_y[i]))

            lineE.set_data(self.planets[2].positions_x[:i],self.planets[2].positions_y[:i])
            pointsE.set_data(self.planets[2].positions_x[i],self.planets[2].positions_y[i])
            textsE.set_position((self.planets[2].positions_x[i],self.planets[2].positions_y[i]))

            lineMa.set_data(self.planets[3].positions_x[:i],self.planets[3].positions_y[:i])
            pointsMa.set_data(self.planets[3].positions_x[i],self.planets[3].positions_y[i])
            textsMa.set_position((self.planets[3].positions_x[i],self.planets[3].positions_y[i]))

            
            return lineM,lineV,lineE,lineMa,pointsM,pointsV,pointsE,pointsMa,textsM,textsV,textsE,textsMa

        anim = animation.FuncAnimation(fig,
                                        func = update,
                                        frames = len(time),
                                        interval = 1,
                                        blit = True)
        plt.show()

        return anim

        
def main():
    
    AU = 1.5e11
    list_planets = ['mercury','venus','earth','mars']
    list_weights = np.array([3.28e23,4.87e24,6e24,3.4e23])/1.9e30
    list_xpos = np.array([0.4,0.7,1.0,1.5])*AU
    list_ypos = [0,0,0,0]
    list_vys = np.array([47360,35000,29290,24000])
    planets = [Planet(name,x,y,0.0,vy,mass) for (name,mass,x,y,vy) in zip(list_planets,list_weights,list_xpos,list_ypos,list_vys)]
    
    


    sun = Star(0,0,1.9e30)


    solar_system = System(sun,planets)

    time = np.arange(0,730)

    
    for t in tqdm(time):

        solar_system.update_planet_positions()


    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for p in solar_system.planets:
        X,Y = p.positions_x,p.positions_y


        ax.plot(X,Y,label = f'{p.name}')

    plt.show()
    plt.legend()
    """
    
    solar_system.animate_solar_system(time)


    return



if __name__ == '__main__':
    main()




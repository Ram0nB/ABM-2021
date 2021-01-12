
from agents import Consumer, Sugar
from model import SugarModel


def main():
    N = 10
    size = 50
    model = SugarModel(N, size, size)
    model.step() 

    
if __name__ == "__main__":
    main()
import asyncio
from generator.generate import main

if __name__ == '__main__':
    print(asyncio.run(main(search_data=['19307000', '19306372'])))

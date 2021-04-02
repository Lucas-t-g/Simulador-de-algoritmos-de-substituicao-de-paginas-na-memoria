import argparse
import sys

class Manager:
    def __init__(self, input):
        input = input.replace("\n", "")
        input = input.split('|')
        self.n_frames = int(input[0])
        self.frames = [False]*self.n_frames
        self.n_pages = int(input[1])
        self.sequential_page_accesses_to_store = input[2].split(' ')
        self.sequential_page_accesses = []
        self.algorithms_page_exchange = dict([('FIFO', 0), ('MRU', 0), ('NUF', 0), ('OPTIMAL', 0)])
        self.FIFO_aux = []
        self.MRU_aux = []
        self.NUF_aux = []

    def reset(self):
        self.sequential_page_accesses = self.sequential_page_accesses_to_store.copy()
        self.frames = [False]*self.n_frames
        self.FIFO_aux = []
        self.MRU_aux = []
        self.NUF_aux = []
    
    def show(self):
        print("Manager -> frame: {} | page: {} | sequnetial_accesses: {}".format(self.n_frames, self.n_pages, self.sequential_page_accesses_to_store))
        print("Frames:", self.frames)

    def output(self):
        # print(Número de trocas de página no algoritmo FIFO|Número de trocas de página no algoritmo MRU|Número de trocas de página no algoritmo NUF|Número de trocas de página no algoritmo ótimo|nome do algoritmo com desempenho mais próximo do ótimo)        
        self.optimal_algorithm()
        self.FIFO_algorithm()
        self.MRU_algorithm()
        self.NUF_algorithm()
        # print(self.algorithms_page_exchange)
        APE_aux = self.algorithms_page_exchange.copy()
        APE_aux.pop('OPTIMAL')
        # encontra o menor valor 
        better = min(APE_aux, key=lambda key: APE_aux[key])
        # testa quantos valores tem o mesmo valor do melhor
        test = [APE_aux[key] == APE_aux[better] for key in APE_aux.keys()]
        if test.count(True) > 1: better = "empate"
        
        print("\n{:>4}|{:>4}|{:>4}|{:>4}|{:>4}".format(self.algorithms_page_exchange['FIFO'], self.algorithms_page_exchange['MRU'], self.algorithms_page_exchange['NUF'], self.algorithms_page_exchange['OPTIMAL'], better), end='')

    def is_this_page_in_frames(self, page):
        # checando se a pagina ja está em alguma moldura
        for frame in self.frames:
            if page == frame:
                return True
        return False
    
    def NUF_algorithm_inside_part(self, page):
        # ver se a pagina ja está em alguma moldura
        if self.is_this_page_in_frames(page):
            self.NUF_aux[self.frames.index(page)] += 1 # adicona um acesso
            return
        else:
            # ver se tem alguma moldura vazia
            self.algorithms_page_exchange['NUF'] += 1
            for i, frame in enumerate(self.frames):
                if frame == False:
                    self.frames[i] = page
                    self.NUF_aux[i] = 1
                    return

            # ver qual página tem a menor frequencia de uso
            index = self.NUF_aux.index(min(self.NUF_aux))
            # print("index: ", index)
            self.frames[index] = page
            self.NUF_aux[index] = 1
                        
            # # ver qual página tem a menor frequencia de uso
            # min_aux = min(self.NUF_aux)
            # indexes = []
            # for i, elem in enumerate(self.NUF_aux):
            #     if elem == min_aux:
            #         indexes.insert(0, i)
            #         # indexes.append(i)
            # # print(self.NUF_aux)
            # # print(indexes)
            # index = indexes[0]
            # # print("index: ", index)
            # self.frames[index] = page
            # self.NUF_aux[index] = 0

    def NUF_algorithm(self):
        self.reset()
        self.NUF_aux = [0]*self.n_frames
        i = 0
        while len(self.sequential_page_accesses) > 0:
            page = self.sequential_page_accesses.pop(0)
            self.NUF_algorithm_inside_part(page)
            # print("page: ", page)
            # print("Frames:", self.frames)
            # print("NUF_aux:", self.NUF_aux)
            # print()

            # # sistema simples de envelhecimento
            # if i % self.n_frames == 0:
            #     for j in range(self.n_frames): self.NUF_aux[j] = int(self.NUF_aux[j]/2)
            i += 1
        # print("Número de trocas de paginas: ", self.algorithms_page_exchange['NUF'])


    def MRU_algorithm_inside_part(self, page):
        # ver se a pagina ja está em alguma moldura
        if self.is_this_page_in_frames(page):
            self.MRU_aux.remove(page)
            self.MRU_aux.insert(0, page)
            return
        else:
            # ver se tem alguma moldura vazia
            self.algorithms_page_exchange['MRU'] += 1
            for i, frame in enumerate(self.frames):
                if frame == False:
                    self.frames[i] = page
                    self.MRU_aux.insert(0, page)
                    return
            
            # ver qual página está a mais tempo sem uso
            removed_page = self.MRU_aux.pop()
            self.MRU_aux.insert(0, page)
            self.frames[self.frames.index(removed_page)] = page

    def MRU_algorithm(self):
        self.reset()
        while len(self.sequential_page_accesses) > 0:
            page = self.sequential_page_accesses.pop(0)
            # print("page: ",page)
            self.MRU_algorithm_inside_part(page)

            # print("frames: ", self.frames)
        #     print("FIFO  : ", self.FIFO_aux)
            # print()
        # print("Número de trocas de paginas: ", self.algorithms_page_exchange['MRU'])

    def FIFO_algorithm_inside_part(self, page):
        # ver se a pagina ja está em alguma moldura
        if self.is_this_page_in_frames(page):
            # self.FIFO_aux.remove(page)
            # self.FIFO_aux.insert(0, page)
            return
        else:
            # ver se tem alguma moldura vazia
            self.algorithms_page_exchange['FIFO'] += 1
            for i, frame in enumerate(self.frames):
                if frame == False:
                    self.frames[i] = page
                    self.FIFO_aux.insert(0, page)
                    return
            
            # ver qual página está a mais tempo em uma moldura
            removed_page = self.FIFO_aux.pop()
            self.FIFO_aux.insert(0, page)
            self.frames[self.frames.index(removed_page)] = page

    def FIFO_algorithm(self):
        self.reset()
        # self.FIFO_aux = []
        while len(self.sequential_page_accesses) > 0:
            page = self.sequential_page_accesses.pop(0)
            # print("page: ",page)
            self.FIFO_algorithm_inside_part(page)

            # print("frames: ", self.frames)
            # print("FIFO  : ", self.FIFO_aux)
            # print()
        # print("Número de trocas de paginas: ", self.algorithms_page_exchange['FIFO'])

    def optimal_algorithm_inside_part(self, page):
        # ver se a pagina ja está em alguma moldura
        if self.is_this_page_in_frames(page):
            return
        else:
            # ver se tem alguma moldura vazia
            self.algorithms_page_exchange['OPTIMAL'] += 1
            for i, frame in enumerate(self.frames):
                if frame == False:
                    self.frames[i] = page
                    return

            #  ver qual moldura tem a página que está mais longe de ser chamada
            distance_to_be_called = [0]*self.n_frames
            for i, frame in enumerate(self.frames):
                for aux_page in self.sequential_page_accesses:
                    if frame == aux_page:
                        break
                    distance_to_be_called[i] += 1
                #ver se a moldura tem uma pagina que nunca sera chamada novamente
                if distance_to_be_called[i] == len(self.sequential_page_accesses):
                    # print("dis: ", distance_to_be_called[i],"tam: ", len(self.sequential_page_accesses))
                    # print(self.frames[i], "nunca é chamada novamente")
                    self.frames[i] = page
                    return
            index = distance_to_be_called.index(max(distance_to_be_called))
            # print("index: ", index)
            self.frames[index] = page
            # print("dtbc: ", distance_to_be_called)
    
    def optimal_algorithm(self):
        self.reset()
        while len(self.sequential_page_accesses) > 0:
            page = self.sequential_page_accesses.pop(0)
            # print("page: ",page)
            self.optimal_algorithm_inside_part(page)
            
            # print(self.frames)
        # print("Número de trocas de paginas: ", self.algorithms_page_exchange['OPTIMAL'])

def main():
    arq = open(path, "r").readlines()
    print('FIFO| MRU| NUF|OPTIMAL', end='')
    for i, line in enumerate(arq):
        # print("\nlinha:", i)
        manager = Manager(line)
        manager.output()

if __name__ == '__main__':
    # aqui são definidos as configurações que se recebe por argumento quando executa o código.
    print("em caso de duvidas, execute com 'python3 main.py -h'", file=sys.stderr)
    parser = argparse.ArgumentParser(description = "Simulador de algoritmos de substituição de páginas na memória {:>>11} by: Lucas T. G.".format(''))
    parser.add_argument('--arquivo', '-a', action = 'store', dest = 'path', 
                    required=True, help = "Arquivo e/ou diretorio com os dados de entrada(este argumento é necessário).")
    
    args = parser.parse_args()
    path = args.path
    main()
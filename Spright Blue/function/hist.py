def historyWrite(userAuthor:str, urlImage:str, folder, calendario, serverName, serverID):
    with open('arq/hist.txt', 'a+') as text_file:
        
        historico = f"""User {userAuthor} salvou a imagem [{urlImage}] | Pasta:[{folder}] | Data de uso: {calendario} | Servidor: {serverName}[{serverID}]\n\n"""
		
        text_file.write(f"{historico}")
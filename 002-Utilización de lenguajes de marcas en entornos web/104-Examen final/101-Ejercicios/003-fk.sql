ALTER TABLE Piezas
ADD CONSTRAINT fk_piezas_categorias
FOREIGN KEY (id_categoria) REFERENCES Categorias(identificador)
ON DELETE CASCADE
ON UPDATE CASCADE;

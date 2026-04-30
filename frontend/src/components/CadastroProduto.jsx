import { useState } from 'react';

function CadastroProduto({ onCadastroSuccess }) {
  const [name, setName] = useState('')
  const [price, setPrice] = useState('');
  const [quantity, setQuantity] = useState('');
  const [image, setImage] = useState('');
  const [mensagem, setMensagem] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const dadosProduto = {
      name: name,
      price: price,
      quantity: quantity,
      image: image
    };

    try {
      const resposta = await fetch('http://localhost:5000/product', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(dadosProduto),
      });

      const dados = await resposta.json();

      if (resposta.ok) {
        setMensagem('Produto cadastrado com sucesso!');
        if (onCadastroSuccess) onCadastroSuccess();

        setName('');
        setPrice('');
        setQuantity('');
        setImage('');
      } else {
        setMensagem(dados.erro || 'Falha ao cadastrar o produto.');
      }
    } catch (erro) {
      console.error('Erro de conexão:', erro);
      setMensagem('Não foi possível conectar com o servidor. Verifique se o backend está rodando e se o CORS está configurado.');
    }
  };

  return (
    <div className="auth-card" style={{ margin: '0 auto' }}>
      <h2 style={{ marginTop: 0, textAlign: 'center' }}>Cadastro de Produto</h2>
      <p style={{ fontSize: '14px', color: '#aaa', textAlign: 'center', marginBottom: '20px' }}>
        Preencha os dados do produto para adicionar ao estoque.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Nome do Produto:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="dark-input"
          />
        </div>

        <div className="form-group">
          <label>Preço:</label>
          <input
            type="number"
            step="0.01"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
            className="dark-input"
          />
        </div>

        <div className="form-group">
          <label>Quantidade:</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
            className="dark-input"
          />
        </div>

        <div className="form-group">
          <label>URL da Imagem:</label>
          <input
            type="url"
            value={image}
            onChange={(e) => setImage(e.target.value)}
            required
            className="dark-input"
          />
        </div>

        <button type="submit" className="btn-success">
          Cadastrar Produto
        </button>
      </form>

      {mensagem && (
        <p style={{ marginTop: '15px', textAlign: 'center', color: mensagem.includes('sucesso') ? '#28a745' : '#dc3545' }}>
          {mensagem}
        </p>
      )}
    </div>
  );
}

export default CadastroProduto;

import { useState } from 'react';

function CadastroProduto({ onCadastroSuccess }) {
  const [name, setName] = useState('')
  const [price, setPrice] = useState('');
  const [quantity, setQuantity] = useState('');
  const [image, setImage] = useState('');

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
        },
        body: JSON.stringify(dadosProduto),
      });

      const dados = await resposta.json();

      if (resposta.ok) {
        alert('Produto cadastrado com sucesso!');
        if (onCadastroSuccess) onCadastroSuccess();
    
        setName('');
        setPrice('');
        setQuantity('');
        setImage('');
      } else {
        alert(`Erro: ${dados.erro || 'Falha ao cadastrar'}`);
      }
    } catch (erro) {
      console.error('Erro de conexão:', erro);
      alert('Não foi possível conectar com o servidor. Verifique se o backend está rodando e se o CORS está configurado.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', fontFamily: 'sans-serif' }}>
      <h2>Cadastro de Produto</h2>
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        
        <div>
          <label>Nome do Produto:</label>
          <input 
            type="text" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div>
          <label>Preço:</label>
          <input 
            type="number" 
            step="0.01"
            value={price} 
            onChange={(e) => setPrice(e.target.value)} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div>
          <label>Quantidade:</label>
          <input 
            type="number" 
            value={quantity} 
            onChange={(e) => setQuantity(e.target.value)} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div>
          <label>URL da Imagem:</label>
          <input 
            type="url" 
            value={image} 
            onChange={(e) => setImage(e.target.value)} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <button 
          type="submit" 
          style={{ padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          Cadastrar Produto
        </button>
      </form>
    </div>
  );
}

export default CadastroProduto;
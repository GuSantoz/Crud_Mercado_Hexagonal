import { useState, useEffect } from 'react';

function ListarProdutos() {
  const [produtos, setProdutos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  useEffect(() => {
    buscarProdutos();
  }, []);

  const buscarProdutos = async () => {
    setCarregando(true);
    setErro('');
    
    try {
      const resposta = await fetch('http://localhost:5000/product', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      const dados = await resposta.json();

      if (resposta.ok) {
        setProdutos(dados.usuarios || []);
      } else {
        setErro(dados.erro || 'Erro ao buscar produtos');
      }
    } catch (erro) {
      console.error('Erro de conexão:', erro);
      setErro('Não foi possível conectar com o servidor.');
    } finally {
      setCarregando(false);
    }
  };

  if (carregando) {
    return <div style={{ textAlign: 'center', padding: '20px' }}>Carregando produtos...</div>;
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '20px auto', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Todos os Produtos</h2>
        <button 
          onClick={buscarProdutos}
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#28a745', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            cursor: 'pointer'
          }}
        >
          🔄 Atualizar
        </button>
      </div>

      {erro && (
        <div style={{ 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          padding: '12px', 
          borderRadius: '4px', 
          marginBottom: '20px' 
        }}>
          {erro}
        </div>
      )}

      {produtos.length === 0 ? (
        <div style={{ 
          backgroundColor: '#e2e3e5', 
          padding: '20px', 
          borderRadius: '4px', 
          textAlign: 'center' 
        }}>
          <p>Nenhum produto cadastrado ainda.</p>
        </div>
      ) : (
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', 
          gap: '20px' 
        }}>
          {produtos.map((produto) => (
            <div 
              key={produto.id}
              style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '15px',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                backgroundColor: '#fff'
              }}
            >
              <img 
                src={produto.image} 
                alt={produto.name}
                style={{
                  width: '100%',
                  height: '200px',
                  objectFit: 'cover',
                  borderRadius: '4px',
                  marginBottom: '10px'
                }}
                onError={(e) => { e.target.src = 'https://via.placeholder.com/200'; }}
              />
              <h3 style={{ margin: '10px 0 5px 0', fontSize: '18px', color: '#333' }}>{produto.name}</h3>
              <p style={{ margin: '5px 0', fontSize: '16px', fontWeight: 'bold', color: '#28a745' }}>
                R$ {parseFloat(produto.price).toFixed(2)}
              </p>
              <p style={{ margin: '5px 0', fontSize: '14px', color: '#333' }}>
                <strong>Estoque:</strong> {produto.quantity} unidades
              </p>
              <p style={{ margin: '5px 0', fontSize: '14px', color: '#333' }}>
                <strong>Status:</strong> {produto.status ? '✅ Ativo' : '❌ Inativo'}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ListarProdutos;

import { useState, useEffect } from 'react';
import EditarProduto from './EditarProduto';

function ListarProdutos() {
  const [produtos, setProdutos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');
  const [produtoEditado, setProdutoEditado] = useState(null);
  const [produtoParaDeletar, setProdutoParaDeletar] = useState(null);

  useEffect(() => {
    if (produtoEditado || produtoParaDeletar) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [produtoEditado, produtoParaDeletar]);

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

  const handleDeleteConfirm = async () => {
    if (!produtoParaDeletar) return;

    const token = localStorage.getItem('token');
    if (!token) {
      setErro('Você precisa estar logado para deletar o produto.');
      setProdutoParaDeletar(null);
      return;
    }

    try {
      const resposta = await fetch(`http://localhost:5000/product/${produtoParaDeletar.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });

      if (resposta.ok) {
        setProdutoParaDeletar(null);
        buscarProdutos();
      } else {
        const dados = await resposta.json();
        setErro(dados.erro || 'Erro ao deletar o produto');
      }
    } catch (erro) {
      console.error('Erro de conexão:', erro);
      setErro('Não foi possível conectar com o servidor.');
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
                backgroundColor: '#fff',
                position: 'relative'
              }}
            >
              <button
                onClick={() => setProdutoEditado(produto)}
                style={{
                  position: 'absolute',
                  top: '12px',
                  right: '12px',
                  background: '#007bff',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '50%',
                  width: '34px',
                  height: '34px',
                  cursor: 'pointer',
                  fontSize: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
                title="Editar produto"
              >
                ✏️
              </button>
              <button
                onClick={() => setProdutoParaDeletar(produto)}
                style={{
                  position: 'absolute',
                  top: '12px',
                  right: '50px',
                  background: '#dc3545',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '50%',
                  width: '34px',
                  height: '34px',
                  cursor: 'pointer',
                  fontSize: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
                title="Deletar produto"
              >
                🗑️
              </button>
              <img 
                src={`http://localhost:5000/uploads/${produto.image}`} 
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
                <strong>Cod Produto:</strong> {produto.id}
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

      {produtoEditado && (
        <div style={{
          position: 'fixed',
          inset: 0,
          backgroundColor: 'rgba(0,0,0,0.65)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000,
          padding: '20px',
          overflow: 'hidden'
        }}>
          <div style={{ display: 'inline-block', maxWidth: '600px', maxHeight: 'calc(100vh - 40px)', position: 'relative', overflowY: 'auto', boxSizing: 'border-box' }}>
            <button
              onClick={() => setProdutoEditado(null)}
              style={{
                position: 'absolute',
                top: '10px',
                right: '10px',
                background: '#dc3545',
                color: '#fff',
                border: 'none',
                borderRadius: '50%',
                width: '36px',
                height: '36px',
                cursor: 'pointer',
                fontSize: '18px',
                zIndex: 1100
              }}
            >
              ✖
            </button>
            <EditarProduto
              produto={produtoEditado}
              onCancel={() => setProdutoEditado(null)}
              onUpdateSuccess={() => {
                setProdutoEditado(null);
                buscarProdutos();
              }}
            />
          </div>
        </div>
      )}

      {produtoParaDeletar && (
        <div style={{
          position: 'fixed',
          inset: 0,
          backgroundColor: 'rgba(0,0,0,0.65)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div style={{
            backgroundColor: '#fff',
            padding: '30px',
            borderRadius: '8px',
            maxWidth: '400px',
            textAlign: 'center',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
          }}>
            <h3 style={{ marginTop: 0, color: '#333' }}>Confirmar Exclusão</h3>
            <p style={{ color: '#666', marginBottom: '20px' }}>
              Tem certeza que deseja deletar o produto <strong>"{produtoParaDeletar.name}"</strong>?
            </p>
            <p style={{ color: '#999', fontSize: '14px', marginBottom: '30px' }}>
              Esta ação não pode ser desfeita.
            </p>
            <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
              <button
                onClick={() => setProdutoParaDeletar(null)}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#6c757d',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '16px'
                }}
              >
                Cancelar
              </button>
              <button
                onClick={handleDeleteConfirm}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#dc3545',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '16px'
                }}
              >
                Deletar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ListarProdutos;

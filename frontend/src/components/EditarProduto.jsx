import { useState, useEffect } from 'react';
import '../App.css';

const EditarProduto = ({ produto, onCancel, onUpdateSuccess }) => {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [quantity, setQuantity] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagemAtual, setImagemAtual] = useState('');
  const [status, setStatus] = useState(false);
  const [mensagem, setMensagem] = useState('');

  const handleFileChange = (e) => {
    setImageFile(e.target.files[0]);
  };

  useEffect(() => {
    if (produto) {
      setName(produto.name || '');
      setPrice(produto.price != null ? produto.price : '');
      setQuantity(produto.quantity != null ? produto.quantity : '');
      setImagemAtual(produto.image || '');
      setImageFile(null);
      setStatus(!!produto.status);
      setMensagem('');
    }
  }, [produto]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');

    if (!token) {
      setMensagem('Você precisa estar logado para editar o produto.');
      return;
    }

    if (!produto || !produto.id) {
      setMensagem('Produto inválido.');
      return;
    }

    const formData = new FormData();
    formData.append('id', produto.id);
    formData.append('name', name);
    formData.append('price', price);
    formData.append('quantity', quantity);
    formData.append('status', status);
    
    // Se um novo arquivo foi selecionado, envia o arquivo; caso contrário, envia o nome da imagem atual
    if (imageFile) {
      formData.append('image', imageFile);
    } else {
      formData.append('image', imagemAtual);
    }

    try {
      const response = await fetch('http://localhost:5000/product', {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        setMensagem('Produto atualizado com sucesso!');
        if (onUpdateSuccess) onUpdateSuccess();
      } else {
        setMensagem(result.erro || result.message || 'Erro ao atualizar o produto.');
      }
    } catch (error) {
      setMensagem('Erro de conexão com o servidor.');
    }
  };

  return (
    <div className="auth-card" style={{ margin: '0 auto', maxWidth: '500px' }}>
      <h2 style={{ marginTop: 0, textAlign: 'center' }}>Editar Produto</h2>
      <p style={{ fontSize: '14px', color: '#aaa', textAlign: 'center', marginBottom: '20px' }}>
        Atualize os dados do produto abaixo. O ID não pode ser alterado.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>ID do Produto:</label>
          <input
            type="text"
            value={produto?.id || ''}
            readOnly
            className="dark-input"
          />
        </div>

        <div className="form-group">
          <label>Nome do Produto:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
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
            className="dark-input"
          />
        </div>

        <div className="form-group">
          <label>Quantidade:</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="dark-input"
          />
        </div>

        <div className="form-group">
          <label>Imagem:</label>
          {imagemAtual && !imageFile && (
            <div style={{ marginBottom: '10px' }}>
              <p style={{ fontSize: '12px', color: '#999', margin: '0 0 8px 0' }}>Imagem atual:</p>
              <img
                src={`http://localhost:5000/uploads/${imagemAtual}`}
                alt="Preview"
                style={{
                  maxWidth: '150px',
                  maxHeight: '150px',
                  borderRadius: '4px',
                  objectFit: 'cover',
                  border: '1px solid #ddd',
                  padding: '4px'
                }}
                onError={(e) => { e.target.style.display = 'none'; }}
              />
            </div>
          )}
          {imageFile && (
            <div style={{ marginBottom: '10px' }}>
              <p style={{ fontSize: '12px', color: '#28a745', margin: '0 0 8px 0' }}>✓ Nova imagem selecionada: {imageFile.name}</p>
            </div>
          )}
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="dark-input"
          />
        </div>

        <div className="form-group" style={{ flexDirection: 'row', alignItems: 'center' }}>
          <label>Status:</label>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <input
              type="checkbox"
              checked={status}
              onChange={(e) => setStatus(e.target.checked)}
            />
            <span style={{ color: '#aaa' }}>{status ? 'Ativo' : 'Inativo'}</span>
          </div>
        </div>

        <button type="submit" className="btn-success">
          Salvar Alterações
        </button>
      </form>

      <button
        onClick={onCancel}
        style={{
          marginTop: '12px',
          width: '100%',
          padding: '10px',
          backgroundColor: '#6c757d',
          color: '#fff',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
      >
        Cancelar
      </button>

      {mensagem && (
        <p style={{ marginTop: '15px', textAlign: 'center', color: mensagem.includes('sucesso') ? '#28a745' : '#dc3545' }}>
          {mensagem}
        </p>
      )}
    </div>
  );
};

export default EditarProduto;

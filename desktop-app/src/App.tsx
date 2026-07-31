import { useState, useRef, useEffect } from 'react'
import './App.css'

type Tool = 'none' | 'brush' | 'eraser';

function App() {
  const [originalFile, setOriginalFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTool, setActiveTool] = useState<Tool>('none');
  const [brushSize, setBrushSize] = useState(20);
  
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const originalImageRef = useRef<HTMLImageElement | null>(null);
  const maskImageRef = useRef<HTMLImageElement | null>(null);

  const isDrawing = useRef(false);

  const [selectedModel, setSelectedModel] = useState('birefnet-general');

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setOriginalFile(file);
      
      // Load original image to canvas
      const img = new Image();
      img.onload = () => {
        originalImageRef.current = img;
        maskImageRef.current = null; // reset mask
        drawCanvas();
      };
      img.src = URL.createObjectURL(file);
    }
  };

  const removeBackground = async () => {
    if (!originalFile) return;
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', originalFile);

      // Call the local python API we bundled
      const response = await fetch(`http://127.0.0.1:8000/api/remove-bg?model=${selectedModel}`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const img = new Image();
        img.onload = () => {
          maskImageRef.current = img;
          drawCanvas();
        };
        img.src = URL.createObjectURL(blob);
      } else {
        alert("Failed to remove background");
      }
    } catch (error) {
      console.error(error);
      alert("Error calling local API. Ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const drawCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const img = originalImageRef.current;
    if (!img) return;

    // Set canvas dimensions
    canvas.width = img.width;
    canvas.height = img.height;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (maskImageRef.current) {
      // If we have a mask, draw the masked image
      ctx.drawImage(maskImageRef.current, 0, 0);
    } else {
      // Draw original
      ctx.drawImage(img, 0, 0);
    }
  };

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (activeTool === 'none') return;
    isDrawing.current = true;
    draw(e);
  };

  const stopDrawing = () => {
    isDrawing.current = false;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (ctx) ctx.beginPath(); // Reset path
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing.current || activeTool === 'none' || !maskImageRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;

    const rect = canvas.getBoundingClientRect();
    
    // Calculate scale because canvas display size !== logical size
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    
    if (activeTool === 'eraser') {
      // Erase from the masked image (make transparent)
      ctx.globalCompositeOperation = 'destination-out';
      ctx.lineTo(x, y);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x, y);
    } else if (activeTool === 'brush' && originalImageRef.current) {
      // Restore original image content
      ctx.globalCompositeOperation = 'source-over';
      ctx.save();
      ctx.beginPath();
      ctx.arc(x, y, brushSize / 2, 0, Math.PI * 2);
      ctx.clip();
      ctx.drawImage(originalImageRef.current, 0, 0);
      ctx.restore();
      ctx.beginPath(); 
    }
  };

  const handleSave = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const url = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = 'edited_image.png';
    link.href = url;
    link.click();
  };

  return (
    <div className="app-container">
      <div className="sidebar">
        <h1 className="title">BG Remover Pro</h1>
        
        <label className="upload-btn">
          {originalFile ? originalFile.name : 'Choose Image'}
          <input type="file" accept="image/*" hidden onChange={handleFileUpload} />
        </label>

        <div className="model-selector-section">
          <label htmlFor="model-select">AI Model:</label>
          <select 
            id="model-select" 
            className="model-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
          >
            <option value="birefnet-general">⭐ BiRefNet SOTA (Best for Landscapes & Detail)</option>
            <option value="birefnet-hrs">⭐ BiRefNet High-Res (Ultra Sharp)</option>
            <option value="birefnet-portrait">BiRefNet Portrait (Ultra Fine Hair)</option>
            <option value="sky-remover">Sky Remover (Landscapes & Mountains)</option>
            <option value="u2net">U2Net (Standard Objects)</option>
            <option value="isnet-general-use">ISNet General</option>
            <option value="silueta">Silueta (Fast & Lightweight)</option>
          </select>
        </div>

        <button 
          className="action-btn" 
          onClick={removeBackground}
          disabled={!originalFile || loading}
        >
          {loading ? 'Processing AI...' : '✨ Auto Remove Background'}
        </button>

        <div className="tools-section">
          <h3>Touch-up Tools</h3>
          <div className="tool-row">
            <button 
              className={`tool-btn ${activeTool === 'eraser' ? 'active' : ''}`}
              onClick={() => setActiveTool(activeTool === 'eraser' ? 'none' : 'eraser')}
            >
              Eraser
            </button>
            <button 
              className={`tool-btn ${activeTool === 'brush' ? 'active' : ''}`}
              onClick={() => setActiveTool(activeTool === 'brush' ? 'none' : 'brush')}
            >
              Restore Brush
            </button>
          </div>
          
          <label>Brush Size: {brushSize}px</label>
          <input 
            type="range" 
            min="5" 
            max="100" 
            value={brushSize} 
            onChange={(e) => setBrushSize(parseInt(e.target.value))}
          />
        </div>

        <button className="action-btn" onClick={handleSave} style={{marginTop: 'auto'}}>
          💾 Save Image
        </button>
      </div>

      <div className="canvas-area">
        <canvas 
          ref={canvasRef}
          onMouseDown={startDrawing}
          onMouseUp={stopDrawing}
          onMouseOut={stopDrawing}
          onMouseMove={draw}
          style={{ maxWidth: '90%', maxHeight: '90%', objectFit: 'contain' }}
        />
      </div>
    </div>
  )
}

export default App

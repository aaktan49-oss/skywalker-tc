import React, { useState, useRef, useCallback } from 'react';

const FileUploader = ({ 
  onFileUploaded, 
  accept = "image/*,video/*,.pdf,.doc,.docx", 
  category = null,
  multiple = false,
  className = ""
}) => {
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef(null);
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const handleFileSelect = (files) => {
    if (!files || files.length === 0) return;

    const fileList = Array.from(files);

    if (multiple) {
      fileList.forEach(file => uploadFile(file));
    } else {
      uploadFile(fileList[0]);
    }
  };

  const uploadFile = async (file) => {
    setUploading(true);
    setUploadProgress(0);

    try {
      const token = localStorage.getItem('portal_token');
      const formData = new FormData();
      formData.append('file', file);
      if (category) formData.append('category', category);

      // Use XMLHttpRequest for progress tracking
      const xhr = new XMLHttpRequest();
      
      return new Promise((resolve, reject) => {
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const progress = Math.round((e.loaded / e.total) * 100);
            setUploadProgress(progress);
          }
        });

        xhr.addEventListener('load', () => {
          if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.success) {
              if (onFileUploaded) {
                onFileUploaded(response.file);
              }
              resolve(response);
            } else {
              reject(new Error(response.detail || 'Upload failed'));
            }
          } else {
            reject(new Error(`Upload failed: ${xhr.status}`));
          }
          setUploading(false);
          setUploadProgress(0);
        });

        xhr.addEventListener('error', () => {
          reject(new Error('Upload failed'));
          setUploading(false);
          setUploadProgress(0);
        });

        xhr.open('POST', `${API_BASE}/api/files/upload`);
        xhr.setRequestHeader('Authorization', `Bearer ${token}`);
        xhr.send(formData);
      });

    } catch (error) {
      console.error('Upload error:', error);
      alert(`Upload hatası: ${error.message}`);
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files);
    }
  }, []);

  const openFileSelector = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className={`relative ${className}`}>
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        multiple={multiple}
        onChange={(e) => handleFileSelect(e.target.files)}
        className="hidden"
      />

      {/* Drop zone */}
      <div
        className={`
          border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all duration-200
          ${dragActive 
            ? 'border-purple-500 bg-purple-50' 
            : 'border-gray-300 hover:border-purple-400 hover:bg-gray-50'
          }
          ${uploading ? 'pointer-events-none opacity-50' : ''}
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={openFileSelector}
      >
        {uploading ? (
          <div className="space-y-4">
            <div className="text-4xl">⏳</div>
            <div>
              <div className="text-lg font-medium text-gray-900 mb-2">
                Dosya yükleniyor...
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
              <div className="text-sm text-gray-500 mt-1">
                %{uploadProgress}
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-4xl text-gray-400">
              {category === 'image' ? '🖼️' : category === 'video' ? '🎥' : '📁'}
            </div>
            <div>
              <div className="text-lg font-medium text-gray-900 mb-2">
                Dosya yüklemek için tıklayın veya sürükleyip bırakın
              </div>
              <div className="text-sm text-gray-500 space-y-1">
                <p>Desteklenen formatlar: JPG, PNG, GIF, MP4, PDF</p>
                <p>Maksimum boyut: {(maxSize / 1024 / 1024).toFixed(1)}MB</p>
                {multiple && <p>Birden fazla dosya seçebilirsiniz</p>}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUploader;
import React, { useState, useEffect, useCallback } from 'react';
import { Layers, Wand2 } from 'lucide-react';
import UploadZone from './components/UploadZone';
import Controls from './components/Controls';
import { generateStencil } from './utils/imageProcessor';
import { StencilSettings } from './types';

const INITIAL_SETTINGS: StencilSettings = {
  lowThreshold: 30,
  highThreshold: 100,
  blurRadius: 2,
  inverted: true
};

function App() {
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [settings, setSettings] = useState<StencilSettings>(INITIAL_SETTINGS);
  const [isProcessing, setIsProcessing] = useState(false);

  // Debounce logic for processing to avoid UI lag on slider drag
  useEffect(() => {
    if (!originalImage) return;

    const timer = setTimeout(async () => {
      setIsProcessing(true);
      try {
        const result = await generateStencil(
          originalImage,
          settings.lowThreshold,
          settings.highThreshold,
          settings.blurRadius
        );
        setProcessedImage(result);
      } catch (error) {
        console.error("Processing failed", error);
      } finally {
        setIsProcessing(false);
      }
    }, 150); // 150ms debounce

    return () => clearTimeout(timer);
  }, [originalImage, settings.lowThreshold, settings.highThreshold, settings.blurRadius]);

  const handleImageSelect = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        setOriginalImage(e.target.result as string);
        // Reset processed image to show loading state effectively
        setProcessedImage(null); 
      }
    };
    reader.readAsDataURL(file);
  };

  const handleSettingChange = (key: keyof StencilSettings, value: number) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleReset = () => {
    setOriginalImage(null);
    setProcessedImage(null);
    setSettings(INITIAL_SETTINGS);
  };

  const handleDownload = () => {
    if (!processedImage) return;
    const link = document.createElement('a');
    link.download = 'inkflow-stencil.png';
    link.href = processedImage;
    link.click();
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 pb-20">
      {/* Header */}
      <header className="bg-slate-950/50 border-b border-slate-800 sticky top-0 z-10 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
          <div className="bg-gradient-to-br from-teal-500 to-emerald-600 p-2 rounded-lg shadow-lg shadow-teal-900/30">
            <Layers className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-200 to-emerald-400">
              InkFlow
            </h1>
            <p className="text-xs text-slate-500 font-medium tracking-wide">TATTOO STENCIL GENERATOR</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-10">
        {!originalImage ? (
          <div className="flex flex-col items-center justify-center min-h-[60vh]">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold text-white mb-4">Turn Photos into Stencils.</h2>
              <p className="text-slate-400 max-w-md mx-auto">
                Upload any reference photo and instantly generate a clean, printable line-work stencil for tattooing.
              </p>
            </div>
            <UploadZone onImageSelected={handleImageSelect} />
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Controls Sidebar */}
            <div className="lg:col-span-1">
              <Controls 
                settings={settings}
                onSettingChange={handleSettingChange}
                onReset={handleReset}
                onDownload={handleDownload}
                isProcessing={isProcessing}
                hasResult={!!processedImage}
              />
            </div>

            {/* Preview Area */}
            <div className="lg:col-span-3 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Original View */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-400 uppercase tracking-wider">Original</span>
                  </div>
                  <div className="aspect-[3/4] bg-slate-800 rounded-xl overflow-hidden border border-slate-700 relative">
                    <img 
                      src={originalImage} 
                      alt="Original" 
                      className="w-full h-full object-contain"
                    />
                  </div>
                </div>

                {/* Stencil View */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-teal-400 uppercase tracking-wider flex items-center gap-2">
                      <Wand2 className="w-4 h-4" />
                      Stencil Result
                    </span>
                    {isProcessing && <span className="text-xs text-emerald-500 animate-pulse">Processing...</span>}
                  </div>
                  <div className="aspect-[3/4] bg-white rounded-xl overflow-hidden border border-slate-700 relative flex items-center justify-center">
                    {processedImage ? (
                      <img 
                        src={processedImage} 
                        alt="Stencil" 
                        className={`w-full h-full object-contain transition-opacity duration-300 ${isProcessing ? 'opacity-80' : 'opacity-100'}`}
                      />
                    ) : (
                      <div className="flex flex-col items-center gap-2 text-slate-300">
                        <div className="w-8 h-8 border-4 border-slate-300 border-t-teal-500 rounded-full animate-spin"></div>
                        <span className="text-sm">Processing Edges...</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

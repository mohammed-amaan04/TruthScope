import { useState } from 'react'
import { RefreshCw, Image as ImageIcon, CheckCircle, XCircle } from 'lucide-react'

const ImageTestPage = () => {
  const [imageTests, setImageTests] = useState<{ [key: string]: 'loading' | 'success' | 'error' }>({})

  const testImages = [
    {
      id: 'unsplash-politics',
      url: 'https://source.unsplash.com/400x250/?government,politics&sig=1',
      title: 'Politics Image Test',
      category: 'politics'
    },
    {
      id: 'unsplash-economics',
      url: 'https://source.unsplash.com/400x250/?business,finance&sig=2',
      title: 'Economics Image Test',
      category: 'economics'
    },
    {
      id: 'unsplash-celebrity',
      url: 'https://source.unsplash.com/400x250/?entertainment,celebrity&sig=3',
      title: 'Celebrity Image Test',
      category: 'celebrity'
    },
    {
      id: 'unsplash-sports',
      url: 'https://source.unsplash.com/400x250/?sports,stadium&sig=4',
      title: 'Sports Image Test',
      category: 'sports'
    },
    {
      id: 'placeholder-reuters',
      url: 'https://via.placeholder.com/400x250/1e40af/ffffff?text=Reuters',
      title: 'Reuters Placeholder',
      category: 'news'
    },
    {
      id: 'placeholder-bbc',
      url: 'https://via.placeholder.com/400x250/cc0000/ffffff?text=BBC',
      title: 'BBC Placeholder',
      category: 'news'
    }
  ]

  const generateSVGPlaceholder = (category: string, title: string) => {
    const categoryColors = {
      politics: '#1e40af',
      economics: '#059669',
      celebrity: '#dc2626',
      sports: '#7c2d12',
      news: '#6b7280'
    }
    
    const color = categoryColors[category as keyof typeof categoryColors] || '#6b7280'
    const initials = title.split(' ').slice(0, 2).map(word => word[0]).join('').toUpperCase()
    
    const svg = `
      <svg width="400" height="250" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="${color}"/>
        <rect x="10" y="10" width="380" height="230" fill="none" stroke="white" stroke-width="2" opacity="0.3"/>
        <text x="50%" y="45%" text-anchor="middle" fill="white" font-size="48" font-weight="bold" font-family="Arial">${initials}</text>
        <text x="50%" y="65%" text-anchor="middle" fill="white" font-size="14" font-family="Arial" opacity="0.8">${category.toUpperCase()}</text>
      </svg>
    `
    
    return `data:image/svg+xml;base64,${btoa(svg)}`
  }

  const handleImageLoad = (id: string) => {
    setImageTests(prev => ({ ...prev, [id]: 'success' }))
  }

  const handleImageError = (id: string) => {
    setImageTests(prev => ({ ...prev, [id]: 'error' }))
  }

  const handleImageLoadStart = (id: string) => {
    setImageTests(prev => ({ ...prev, [id]: 'loading' }))
  }

  const getStatusIcon = (status: 'loading' | 'success' | 'error' | undefined) => {
    switch (status) {
      case 'loading':
        return <RefreshCw className="w-4 h-4 animate-spin text-blue-500" />
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'error':
        return <XCircle className="w-4 h-4 text-red-500" />
      default:
        return <ImageIcon className="w-4 h-4 text-gray-500" />
    }
  }

  const refreshImages = () => {
    setImageTests({})
    // Force reload by adding timestamp
    const timestamp = Date.now()
    testImages.forEach(img => {
      const imgElement = document.getElementById(`img-${img.id}`) as HTMLImageElement
      if (imgElement) {
        imgElement.src = img.url + `&t=${timestamp}`
      }
    })
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <div className="paper-texture newspaper-border p-8 mb-8">
          <h1 className="newspaper-headline-bold text-4xl text-newspaper-black mb-4">
            IMAGE LOADING TEST PAGE
          </h1>
          <div className="newspaper-divider mb-6"></div>
          
          <div className="flex items-center justify-between mb-6">
            <p className="newspaper-body text-newspaper-gray">
              This page tests image loading functionality for the news dashboard.
            </p>
            <button
              onClick={refreshImages}
              className="flex items-center space-x-2 px-4 py-2 bg-newspaper-black text-white hover:bg-newspaper-gray transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Refresh Images</span>
            </button>
          </div>

          {/* External Image Tests */}
          <section className="mb-8">
            <h2 className="newspaper-subheading-bold text-2xl mb-4">External Image Sources</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {testImages.map((test) => (
                <div key={test.id} className="newspaper-border paper-texture overflow-hidden">
                  <div className="news-image-container h-48">
                    <img
                      id={`img-${test.id}`}
                      src={test.url}
                      alt={test.title}
                      className="news-image"
                      onLoadStart={() => handleImageLoadStart(test.id)}
                      onLoad={() => handleImageLoad(test.id)}
                      onError={() => handleImageError(test.id)}
                      loading="lazy"
                    />
                  </div>
                  <div className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="newspaper-body font-semibold">{test.title}</h3>
                      {getStatusIcon(imageTests[test.id])}
                    </div>
                    <p className="text-sm text-newspaper-gray mb-2">
                      Category: {test.category}
                    </p>
                    <p className="text-xs text-newspaper-gray break-all">
                      {test.url}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* SVG Placeholder Tests */}
          <section className="mb-8">
            <h2 className="newspaper-subheading-bold text-2xl mb-4">Generated SVG Placeholders</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {['politics', 'economics', 'celebrity', 'sports'].map((category) => (
                <div key={category} className="newspaper-border paper-texture overflow-hidden">
                  <div className="news-image-container h-32">
                    <img
                      src={generateSVGPlaceholder(category, `${category} news`)}
                      alt={`${category} placeholder`}
                      className="news-image"
                    />
                  </div>
                  <div className="p-3">
                    <h3 className="newspaper-body font-semibold capitalize">{category}</h3>
                    <p className="text-xs text-newspaper-gray">SVG Placeholder</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Layout Test */}
          <section className="mb-8">
            <h2 className="newspaper-subheading-bold text-2xl mb-4">Layout Test (News Dashboard Style)</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Big news item */}
              <div className="md:col-span-2">
                <div className="newspaper-border paper-texture overflow-hidden news-card">
                  <div className="news-image-container h-48">
                    <img
                      src="https://source.unsplash.com/600x300/?newspaper,news&sig=big"
                      alt="Big news item"
                      className="news-image"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                    <div className="absolute bottom-4 left-4">
                      <span className="px-3 py-1 bg-newspaper-accent text-white text-xs font-semibold uppercase tracking-wide rounded">
                        BREAKING
                      </span>
                    </div>
                  </div>
                  <div className="p-6">
                    <h3 className="newspaper-subheading-bold text-xl mb-3">
                      Major News Story with Image
                    </h3>
                    <p className="newspaper-body text-newspaper-gray">
                      This is a test of the big news item layout with proper image containment and responsive design.
                    </p>
                  </div>
                </div>
              </div>

              {/* Smaller news items */}
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="newspaper-border division-bg overflow-hidden news-card">
                    <div className="flex">
                      <div className="news-image-container w-20 h-16 flex-shrink-0">
                        <img
                          src={`https://source.unsplash.com/200x150/?news,article&sig=small${i}`}
                          alt={`Small news ${i}`}
                          className="news-image"
                        />
                      </div>
                      <div className="flex-1 p-3">
                        <h4 className="newspaper-body-bold text-sm mb-1 line-clamp-2">
                          Small News Item {i} with Image
                        </h4>
                        <p className="text-xs text-newspaper-gray line-clamp-2">
                          Testing the smaller news item layout with images that don't leak out.
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Instructions */}
          <div className="division-bg p-6">
            <h3 className="newspaper-subheading text-lg mb-3">Image Loading Features</h3>
            <div className="space-y-2 text-sm text-newspaper-gray">
              <p>✅ <strong>Contained Images:</strong> All images are properly contained within their divisions</p>
              <p>✅ <strong>Fallback System:</strong> SVG placeholders when external images fail</p>
              <p>✅ <strong>Loading States:</strong> Visual feedback during image loading</p>
              <p>✅ <strong>Error Handling:</strong> Graceful fallback for broken images</p>
              <p>✅ <strong>Responsive Design:</strong> Images adapt to different screen sizes</p>
              <p>✅ <strong>Hover Effects:</strong> Smooth image scaling on hover</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ImageTestPage

import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';

const SEOHead = ({ 
  title, 
  description, 
  keywords = [],
  image,
  url,
  article = false,
  publishedTime,
  modifiedTime,
  author
}) => {
  const [siteSettings, setSiteSettings] = useState({});
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    loadSiteSettings();
  }, []);

  const loadSiteSettings = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/site-settings`);
      const data = await response.json();
      if (data && data.length > 0) {
        setSiteSettings(data[0]);
      }
    } catch (error) {
      console.error('Error loading site settings:', error);
    }
  };

  const siteTitle = siteSettings.siteName || 'Skywalker.tc';
  const siteDescription = siteSettings.siteDescription || 'Trendyol E-ticaret Danışmanlık ve Pazarlama Hizmetleri';
  
  const pageTitle = title ? `${title} - ${siteTitle}` : (siteSettings.metaTitle || siteTitle);
  const pageDescription = description || siteSettings.metaDescription || siteDescription;
  const pageKeywords = [...(keywords || []), ...(siteSettings.metaKeywords || [])].join(', ');
  const pageImage = image || siteSettings.ogImage || `${window.location.origin}/logo.png`;
  const pageUrl = url || window.location.href;

  // JSON-LD Structured Data
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": siteTitle,
    "description": siteDescription,
    "url": window.location.origin,
    "logo": siteSettings.logo || `${window.location.origin}/logo.png`,
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": siteSettings.contactPhone,
      "contactType": "customer service",
      "email": siteSettings.contactEmail
    },
    "address": {
      "@type": "PostalAddress",
      "addressLocality": siteSettings.address
    },
    "sameAs": Object.values(siteSettings.socialMedia || {})
  };

  // Article structured data
  const articleStructuredData = article ? {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": title,
    "description": description,
    "image": pageImage,
    "datePublished": publishedTime,
    "dateModified": modifiedTime || publishedTime,
    "author": {
      "@type": "Person",
      "name": author || siteTitle
    },
    "publisher": {
      "@type": "Organization",
      "name": siteTitle,
      "logo": {
        "@type": "ImageObject",
        "url": siteSettings.logo || `${window.location.origin}/logo.png`
      }
    }
  } : null;

  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{pageTitle}</title>
      <meta name="description" content={pageDescription} />
      {pageKeywords && <meta name="keywords" content={pageKeywords} />}
      <meta name="author" content={siteTitle} />
      <meta name="robots" content="index, follow" />
      <link rel="canonical" href={pageUrl} />

      {/* Open Graph / Facebook */}
      <meta property="og:type" content={article ? "article" : "website"} />
      <meta property="og:title" content={siteSettings.ogTitle || pageTitle} />
      <meta property="og:description" content={siteSettings.ogDescription || pageDescription} />
      <meta property="og:image" content={pageImage} />
      <meta property="og:url" content={pageUrl} />
      <meta property="og:site_name" content={siteTitle} />
      <meta property="og:locale" content="tr_TR" />
      
      {article && (
        <>
          <meta property="article:published_time" content={publishedTime} />
          <meta property="article:modified_time" content={modifiedTime || publishedTime} />
          <meta property="article:author" content={author || siteTitle} />
        </>
      )}

      {/* Twitter Card */}
      <meta name="twitter:card" content={siteSettings.twitterCard || "summary_large_image"} />
      <meta name="twitter:title" content={pageTitle} />
      <meta name="twitter:description" content={pageDescription} />
      <meta name="twitter:image" content={pageImage} />
      {siteSettings.twitterSite && <meta name="twitter:site" content={siteSettings.twitterSite} />}
      {siteSettings.twitterCreator && <meta name="twitter:creator" content={siteSettings.twitterCreator} />}

      {/* Search Engine Verification */}
      {siteSettings.googleVerificationCode && (
        <meta name="google-site-verification" content={siteSettings.googleVerificationCode} />
      )}
      {siteSettings.bingVerificationCode && (
        <meta name="msvalidate.01" content={siteSettings.bingVerificationCode} />
      )}
      {siteSettings.yandexVerificationCode && (
        <meta name="yandex-verification" content={siteSettings.yandexVerificationCode} />
      )}
      {siteSettings.metaVerificationCode && (
        <meta name="facebook-domain-verification" content={siteSettings.metaVerificationCode} />
      )}

      {/* Favicon */}
      {siteSettings.favicon && <link rel="icon" href={siteSettings.favicon} />}

      {/* Google Analytics */}
      {siteSettings.googleAnalyticsId && (
        <>
          <script async src={`https://www.googletagmanager.com/gtag/js?id=${siteSettings.googleAnalyticsId}`} />
          <script>
            {`
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${siteSettings.googleAnalyticsId}', {
                page_title: '${pageTitle}',
                page_location: '${pageUrl}'
              });
            `}
          </script>
        </>
      )}

      {/* Google Tag Manager */}
      {siteSettings.googleTagManagerId && (
        <>
          <script>
            {`
              (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
              new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
              j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
              'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
              })(window,document,'script','dataLayer','${siteSettings.googleTagManagerId}');
            `}
          </script>
        </>
      )}

      {/* Facebook Pixel */}
      {siteSettings.facebookPixelId && (
        <>
          <script>
            {`
              !function(f,b,e,v,n,t,s)
              {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
              n.callMethod.apply(n,arguments):n.queue.push(arguments)};
              if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
              n.queue=[];t=b.createElement(e);t.async=!0;
              t.src=v;s=b.getElementsByTagName(e)[0];
              s.parentNode.insertBefore(t,s)}(window,document,'script',
              'https://connect.facebook.net/en_US/fbevents.js');
              fbq('init', '${siteSettings.facebookPixelId}');
              fbq('track', 'PageView');
            `}
          </script>
          <noscript>
            <img height="1" width="1" style={{display: 'none'}} 
                 src={`https://www.facebook.com/tr?id=${siteSettings.facebookPixelId}&ev=PageView&noscript=1`} />
          </noscript>
        </>
      )}

      {/* Google Ads Conversion */}
      {siteSettings.googleAdsId && (
        <>
          <script async src={`https://www.googletagmanager.com/gtag/js?id=${siteSettings.googleAdsId}`} />
          <script>
            {`
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${siteSettings.googleAdsId}');
            `}
          </script>
        </>
      )}

      {/* Structured Data */}
      <script type="application/ld+json">
        {JSON.stringify(structuredData)}
      </script>

      {/* Article Structured Data */}
      {articleStructuredData && (
        <script type="application/ld+json">
          {JSON.stringify(articleStructuredData)}
        </script>
      )}
    </Helmet>
  );
};

export default SEOHead;
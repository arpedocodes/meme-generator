"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Download, ArrowLeft, AlertCircle } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"
import { useRouter } from "next/navigation"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

interface MemeImage {
  id: string
  url: string
  title: string
}

export default function YourMemePage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [images, setImages] = useState<MemeImage[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Function to fetch images from the server
    const loadImages = async () => {
      try {
        // Get image paths from sessionStorage (set during submission)
        const storedImages = sessionStorage.getItem("memeImages")

        if (!storedImages) {
          throw new Error("No image data found. Please create a meme first.")
        }

        // Parse the stored image paths
        const imagePaths: string[] = JSON.parse(storedImages)

        if (!Array.isArray(imagePaths) || imagePaths.length !== 4) {
          throw new Error("Invalid image data received from server.")
        }

        // Map the paths to our image objects with titles
        const imageObjects: MemeImage[] = [
          {
            id: "1",
            url: `http://localhost:8000/${imagePaths[0]}`,
            title: "Annotated Image",
          },
          {
            id: "2",
            url: `http://localhost:8000/${imagePaths[1]}`,
            title: "Original Image",
          },
          {
            id: "3",
            url: `http://localhost:8000/${imagePaths[2]}`,
            title: "Processed Image 1",
          },
          {
            id: "4",
            url: `http://localhost:8000/${imagePaths[3]}`,
            title: "Processed Image 2",
          },
        ]

        // Set the images and stop loading
        setImages(imageObjects)
        setLoading(false)
      } catch (error) {
        console.error("Error loading images:", error)
        setError(error instanceof Error ? error.message : "Failed to load images from server.")
        setLoading(false)
      }
    }

    loadImages()
  }, [])

  const handleDownload = async (image: MemeImage) => {
    try {
      // Fetch the image from the server
      const response = await fetch(image.url)

      if (!response.ok) {
        throw new Error(`Failed to download image: ${response.statusText}`)
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)

      // Create a link element
      const link = document.createElement("a")
      link.href = url
      link.download = `${image.title.toLowerCase().replace(/\s+/g, "-")}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      // Clean up the URL
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error("Error downloading image:", error)
      alert("Failed to download the image. Please try again.")
    }
  }

  const handleGoBack = () => {
    router.push("/")
  }

  // If there's an error, show an error message
  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center p-4 md:p-8">
        <h1 className="text-3xl font-bold mb-6">Your Meme</h1>

        <div className="w-full max-w-5xl">
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>

          <Button onClick={handleGoBack} className="flex items-center gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back to Editor
          </Button>
        </div>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-4 md:p-8">
      <h1 className="text-3xl font-bold mb-2">Your Meme</h1>

      <div className="w-full max-w-5xl">
        <div className="flex justify-between items-center mb-8">
          <Button onClick={handleGoBack} variant="outline" className="flex items-center gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back to Editor
          </Button>

          <p className="text-gray-500">
            {loading
              ? "Generating your meme variations..."
              : "Here are your meme variations. Click on any image to download it."}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {loading
            ? // Loading skeletons
              Array.from({ length: 4 }).map((_, i) => (
                <Card key={i} className="overflow-hidden">
                  <div className="relative aspect-square w-full">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="w-16 h-16 rounded-full border-4 border-gray-300 border-t-gray-600 animate-spin"></div>
                    </div>
                    <Skeleton className="w-full h-full" />
                  </div>
                  <div className="p-4">
                    <Skeleton className="h-6 w-3/4 mb-2" />
                    <Skeleton className="h-10 w-1/3" />
                  </div>
                </Card>
              ))
            : // Actual images
              images.map((image) => (
                <Card key={image.id} className="overflow-hidden group">
                  <div className="relative aspect-square w-full cursor-pointer" onClick={() => handleDownload(image)}>
                    <img
                      src={image.url || "/placeholder.svg"}
                      alt={image.title}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        // Handle image loading errors
                        console.error(`Failed to load image: ${image.url}`)
                        ;(e.target as HTMLImageElement).src = "/placeholder.svg?height=400&width=400"
                        ;(e.target as HTMLImageElement).alt = "Failed to load image"
                      }}
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                      <Download className="text-white w-12 h-12" />
                    </div>
                  </div>
                  <div className="p-4 flex justify-between items-center">
                    <h3 className="font-medium">{image.title}</h3>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDownload(image)
                      }}
                      className="flex items-center gap-1"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </Button>
                  </div>
                </Card>
              ))}
        </div>
      </div>
    </main>
  )
}

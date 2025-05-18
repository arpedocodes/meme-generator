"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Slider } from "@/components/ui/slider"

type AnnotationRectangle = {
  id: string
  left: number
  top: number
  width: number
  height: number
  angle: number
}

interface EditPanelProps {
  rectangle?: AnnotationRectangle
  updateRectangle: (rect: Partial<AnnotationRectangle>) => void
}

export function EditPanel({ rectangle, updateRectangle }: EditPanelProps) {
  if (!rectangle) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Edit Rectangle</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500 text-center py-8">Select a rectangle to edit its properties</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Edit Rectangle</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="x-position">X Position</Label>
            <Input
              id="x-position"
              type="number"
              value={Math.round(rectangle.left)}
              onChange={(e) => updateRectangle({ left: Number(e.target.value) })}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="y-position">Y Position</Label>
            <Input
              id="y-position"
              type="number"
              value={Math.round(rectangle.top)}
              onChange={(e) => updateRectangle({ top: Number(e.target.value) })}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="width">Width</Label>
            <Input
              id="width"
              type="number"
              value={Math.round(rectangle.width)}
              onChange={(e) => updateRectangle({ width: Number(e.target.value) })}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="height">Height</Label>
            <Input
              id="height"
              type="number"
              value={Math.round(rectangle.height)}
              onChange={(e) => updateRectangle({ height: Number(e.target.value) })}
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label>Rotation Angle: {Math.round(rectangle.angle)}°</Label>
          <Slider
            value={[rectangle.angle]}
            min={0}
            max={360}
            step={1}
            onValueChange={(value) => updateRectangle({ angle: value[0] })}
          />
        </div>
      </CardContent>
    </Card>
  )
}

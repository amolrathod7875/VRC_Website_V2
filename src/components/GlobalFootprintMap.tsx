"use client";

import { useEffect, useRef } from "react";

type Marker = {
  cx: number;
  cy: number;
  label: string;
  tooltip?: string;
};

const markers: Marker[] = [
  { cx: 620, cy: 230, label: "Pune (Bhosari), India", tooltip: "Head Office & Factory" },
  { cx: 635, cy: 255, label: "Wai MIDC, India", tooltip: "Wai MIDC Facility" },
  { cx: 240, cy: 180, label: "Barrie, Ontario, Canada", tooltip: "North America" },
  { cx: 470, cy: 190, label: "Germany", tooltip: "European Reach" },
  { cx: 590, cy: 250, label: "Middle East", tooltip: "Export Network" },
];

export function GlobalFootprintMap({ visible }: { visible: boolean }) {
  const mapRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    const svg = mapRef.current;
    if (!svg || !visible) return;

    const paths = svg.querySelectorAll<SVGPathElement>(".continent-path");
    const lines = svg.querySelectorAll<SVGLineElement>(".connection-line");
    const markerCircles = svg.querySelectorAll<SVGCircleElement>(".marker-pulse");

    if (paths.length) {
      paths.forEach((path, i) => {
        const length = path.getTotalLength ? path.getTotalLength() : 600;
        path.style.strokeDasharray = `${length}`;
        path.style.strokeDashoffset = `${length}`;
        path.style.transition = `stroke-dashoffset 1.2s ease-out ${i * 60}ms`;
        requestAnimationFrame(() => {
          path.style.strokeDashoffset = "0";
        });
      });
    }

    if (lines.length) {
      lines.forEach((line, i) => {
        const length = 200;
        line.style.strokeDasharray = `${length}`;
        line.style.strokeDashoffset = `${length}`;
        line.style.transition = `stroke-dashoffset 0.9s ease-out ${400 + i * 140}ms`;
        requestAnimationFrame(() => {
          line.style.strokeDashoffset = "0";
        });
      });
    }

    if (markerCircles.length) {
      markerCircles.forEach((circle, i) => {
        circle.style.animation = `pulse-ring 2.6s ease-out ${600 + i * 180}ms infinite`;
      });
    }
  }, [visible]);

  return (
    <svg
      ref={mapRef}
      viewBox="0 0 1000 520"
      className="h-full w-full"
      preserveAspectRatio="xMidYMid meet"
      aria-hidden="true"
    >
      <defs>
        <radialGradient id="markerGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#1678C8" stopOpacity="0.35" />
          <stop offset="100%" stopColor="#1678C8" stopOpacity="0" />
        </radialGradient>
        <filter id="mapShadow" x="-5%" y="-5%" width="110%" height="110%">
          <feDropShadow dx="0" dy="4" stdDeviation="6" floodColor="#082B4C" floodOpacity="0.12" />
        </filter>
        <style>
          {`
            @keyframes pulse-ring {
              0% { transform: scale(0.9); opacity: 0.7; }
              70% { transform: scale(1.35); opacity: 0; }
              100% { transform: scale(0.9); opacity: 0; }
            }
            .marker-pulse { transform-origin: center; animation-play-state: paused; }
            .marker-pulse.animate { animation-play-state: running; }
          `}
        </style>
      </defs>

      <g filter="url(#mapShadow)">
        <rect x="0" y="0" width="1000" height="520" rx="24" fill="#f4f7fb" />
      </g>

      <g className="continent-paths">
        {/* North America */}
        <path
          className="continent-path"
          d="M 120 120 L 220 100 L 280 110 L 310 140 L 300 180 L 320 200 L 300 230 L 260 240 L 240 260 L 220 250 L 200 270 L 180 260 L 160 240 L 140 220 L 110 200 L 100 170 L 110 140 Z"
          fill="#dbeafe"
          stroke="#93c5fd"
          strokeWidth="1.2"
        />
        {/* Greenland */}
        <path
          className="continent-path"
          d="M 280 80 L 330 70 L 360 90 L 340 120 L 300 130 L 270 110 Z"
          fill="#dbeafe"
          stroke="#93c5fd"
          strokeWidth="1.2"
        />
        {/* South America */}
        <path
          className="continent-path"
          d="M 240 280 L 290 270 L 320 290 L 330 330 L 310 380 L 280 410 L 250 400 L 230 360 L 220 320 L 230 290 Z"
          fill="#dbeafe"
          stroke="#93c5fd"
          strokeWidth="1.2"
        />
        {/* Europe */}
        <path
          className="continent-path"
          d="M 440 130 L 490 120 L 530 130 L 540 160 L 520 190 L 480 200 L 450 190 L 430 160 L 440 130 Z"
          fill="#dbeafe"
          stroke="#93c5fd"
          strokeWidth="1.2"
        />
        {/* Africa */}
        <path
          className="continent-path"
          d="M 440 210 L 500 200 L 550 220 L 560 270 L 540 330 L 500 360 L 460 350 L 430 300 L 420 250 L 440 210 Z"
          fill="#dbeafe"
          stroke="#93c5fd"
          strokeWidth="1.2"
        />
        {/* Asia */}
        <path
          className="continent-path"
          d="M 540 110 L 640 100 L 720 120 L 780 150 L 800 190 L 780 230 L 720 250 L 660 240 L 600 220 L 560 200 L 540 160 L 540 110 Z"
          fill="#dbeafe"
          stroke="#93c5fd"
          strokeWidth="1.2"
        />
        {/* India subcontinent */}
        <path
          className="continent-path"
          d="M 620 220 L 650 210 L 670 230 L 660 270 L 640 290 L 620 280 L 610 250 L 620 220 Z"
          fill="#bfdbfe"
          stroke="#60a5fa"
          strokeWidth="1.4"
        />
        {/* Southeast Asia / Indonesia */}
        <path
          className="continent-path"
          d="M 700 260 L 760 250 L 800 270 L 790 300 L 750 310 L 710 290 L 700 260 Z"
          fill="#dbeafe"
          stroke="#93c5fd"
          strokeWidth="1.2"
        />
        {/* Australia */}
        <path
          className="continent-path"
          d="M 740 330 L 820 320 L 870 340 L 880 380 L 850 410 L 790 420 L 750 400 L 730 360 L 740 330 Z"
          fill="#dbeafe"
          stroke="#93c5fd"
          strokeWidth="1.2"
        />
      </g>

      <g className="connection-lines">
        <line className="connection-line" x1="620" y1="230" x2="240" y2="200" stroke="#1678C8" strokeWidth="1.4" opacity="0.35" strokeDasharray="6 6" />
        <line className="connection-line" x1="620" y1="230" x2="470" y2="190" stroke="#1678C8" strokeWidth="1.4" opacity="0.35" strokeDasharray="6 6" />
        <line className="connection-line" x1="620" y1="230" x2="590" y2="250" stroke="#1678C8" strokeWidth="1.4" opacity="0.35" strokeDasharray="6 6" />
      </g>

      {markers.map((marker) => (
        <g key={marker.label} transform={`translate(${marker.cx}, ${marker.cy})`}>
          <circle className="marker-pulse" cx="0" cy="0" r="18" fill="url(#markerGlow)" />
          <circle cx="0" cy="0" r="7" fill="#1678C8" />
          <circle cx="0" cy="0" r="3.5" fill="#ffffff" />

          <text
            x="0"
            y="-16"
            textAnchor="middle"
            fill="#082B4C"
            fontSize="11"
            fontWeight="600"
            className="select-none"
          >
            {marker.label}
          </text>
          {marker.tooltip && (
            <text
              x="0"
              y="22"
              textAnchor="middle"
              fill="#1565b0"
              fontSize="10"
              className="select-none"
            >
              {marker.tooltip}
            </text>
          )}
        </g>
      ))}
    </svg>
  );
}

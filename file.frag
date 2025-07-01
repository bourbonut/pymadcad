void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
    float rgb = step(0.5, 1.0 - sin(fragCoord.x * 0.1 + 0.1 * fragCoord.y));
    fragColor = vec4(rgb, rgb, rgb, 1.0);
}

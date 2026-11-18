// case.scad — OpenSCAD parametric controller case.
// 가정(명시): Pico 51x21mm, OLED 27x27mm, M3 나사, 공차 0.2mm.
// 슬라이서 검증 없음. STL은 이 파일에서 파생된 간이 형상(VERIFICATION.md 참고).

tol = 0.2;
pico_l = 51; pico_w = 21;
oled = 27;
wall = 2;
inner_l = pico_l + 12 + tol*2;
inner_w = 56;
inner_h = 18;
M3 = 3.2; // clearance hole

module box() {
  difference() {
    cube([inner_l + wall*2, inner_w + wall*2, inner_h + wall]);
    translate([wall, wall, wall]) cube([inner_l, inner_w, inner_h+1]);
    // OLED window (top, z = 0 base -> cut through lid separately; hole in body side for view)
    translate([(inner_l+wall*2)/2 - oled/2, 8, -1]) cube([oled, oled, wall+2]);
    // button holes (3x 6mm tact -> 6.5mm holes)
    for (x = [20, 40, 60])
      translate([x, inner_w + wall*2 - 1, 8]) rotate([90,0,0]) cylinder(d=6.5, h=wall+2, $fn=24);
    // micro usb slot (front)
    translate([(inner_l+wall*2)/2 - 5, -1, 4]) cube([10, wall+2, 6]);
  }
  // M3 posts
  for (x = [wall+4, inner_l+wall-4], y = [wall+4, inner_w+wall-4])
    translate([x, y, wall]) cylinder(d=7, h=6, $fn=24);
}

module lid() {
  difference() {
    translate([0, 0, inner_h + wall]) cube([inner_l + wall*2, inner_w + wall*2, wall]);
    translate([(inner_l+wall*2)/2 - oled/2, 8, inner_h + wall - 1]) cube([oled, oled, wall+2]);
    for (x = [wall+4, inner_l+wall-4], y = [wall+4, inner_w+wall-4])
      translate([x, y, inner_h + wall - 1]) cylinder(d=M3, h=wall+2, $fn=20);
  }
}

box();
translate([0, 0, 0]) lid();

#color_palette
	$color_main_accent: #034AA6
	$color_secondary_accent: #D9910D
	$color_text: #272727
	$color_headings: #272727
	$color_borders: #f6f6f6
	$color_background: #f2f2f2
	
#typography
paragraph
	size: 16
	line_height: 1.2
heading_1
	size: 48
	line_height: 1.4
	
#components
button
	padding_vertical: 10
	padding_horizontal: 20
	background_color: $color_secondary_accent
	border: 0
	
section
	padding_vertical: 80
	background_color: $color_background
	
	
	
#content
@@section
@@heading_1: testowy heading
@@text:  jakiś krótki tekst
@@button: przycisk


@@section
@@heading_1: nagłowek drugiej sekcji
@@text: to jest drugi akapit
@@button: przycisk drugi
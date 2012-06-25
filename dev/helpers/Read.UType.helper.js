/**
 *	@helper readUtype
 *
 *	@param ch utype character
 *
 *	@author Vibhaj Rajan <vibhaj8@gmail.com>
 *
**/
OrbitNote.core.helper.readUtype = function($ch){
	switch($ch){
		case 'S' :
			return 'Student';
		case 'C' :
			return 'Company';
		case 'T' :
			return 'OrbitNote Web';
		default :
			return '';
			break;
	}
}

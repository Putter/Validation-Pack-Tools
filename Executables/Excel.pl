use strict;
use warnings;
use Spreadsheet::WriteExcel;
use Spreadsheet::ParseExcel;
use Cwd;
use Getopt::Long;
use Spreadsheet::XLSX;
use Encode;


our $command;
our $commandTimer = 240;
our $proxyInvocation = undef;
our $num = 0;

our $QGP_pack = undef;
my $excelFile = undef;
our $QGP_pack_type = undef;
my $checkValue;
my $passCtr = 0;
my $subResult = 1;
my @failedTestcases;
my $testCaseName;
my $subTestResultId;
my $projectName = "Global_Pass";
my $timeStamp = $ARGV[0]; #Unique time stamp for this run
my $platformName = undef;
my $virtioConfigFilename = undef;
my $virtioVmClientDetails = undef;


GetOptions(				'QGP_pack=s' => \$QGP_pack,
						'excelFile=s' => \$excelFile,
						'proxy-invocation=s' => \$proxyInvocation,
						'QGP_pack_type=s' => \$QGP_pack_type
			);

my $QGP_pack_initial = $QGP_pack;
my %Father_Pack = (
					"EEEU"    							=> "EUCommon",
					"LatamTelefonicaArgentina"			=> "LatamTelefonica",
					"LatamTelefonicaBrazil"				=> "LatamTelefonica",
					"LatamTelefonicaChile"				=> "LatamTelefonica",
					"LatamTelefonicaColombia"			=> "LatamTelefonica",
					"LatamTelefonicaCostaRica"			=> "LatamTelefonica",
					"LatamTelefonicaEcuador"			=> "LatamTelefonica",
					"LatamTelefonicaElSalvador"			=> "LatamTelefonica",
					"LatamTelefonicaGuatemala"			=> "LatamTelefonica",
					"LatamTelefonicaMexico"				=> "LatamTelefonica",
					"LatamTelefonicaNicaragua"			=> "LatamTelefonica",
					"LatamTelefonicaPanama"				=> "LatamTelefonica",
					"LatamTelefonicaPeru"				=> "LatamTelefonica",
					"LatamTelefonicaUruguay"			=> "LatamTelefonica",
					"LatamTelefonicaVenezuela"			=> "LatamTelefonica",
					"TelefonicaGermany"					=> "EUCommon",
					"TelefonicaSpain"					=> "EUCommon",
					"VodafoneCzech"						=> "VodafoneGroup",
					"VodafoneES"						=> "VodafoneGroup",
					"VodafoneGermany"					=> "VodafoneGroup",
					"VodafoneGreece"					=> "VodafoneGroup",
					"VodafoneHungary"					=> "VodafoneGroup",
					"VodafoneIT"						=> "VodafoneGroup",
					"VodafoneIreland"					=> "VodafoneGroup",
					"VodafoneNetherlands"				=> "VodafoneGroup",
					"VodafonePT"						=> "VodafoneGroup",
					"VodafoneSouthAfrica"				=> "VodafoneGroup",
					"VodafoneTurkey"					=> "VodafoneGroup",
					"VodafoneUK"						=> "VodafoneGroup",
					"VodafoneGroup"						=> "EUCommon",
					"CherryCambodia"					=> "CherryCommon",
					"CherryLaos"						=> "CherryCommon",
					"CherryMyanmar"						=> "CherryCommon",
					"CherryPhilippines"					=> "CherryCommon",
					"CherryThailand"					=> "CherryCommon",
					"OrangeBelgium"						=> "OrangeCommon",
					"OrangeFrance"						=> "OrangeCommon",
					"OrangeMoldavia"					=> "OrangeCommon",
					"OrangePoland"						=> "OrangeCommon",
					"OrangeRomania"						=> "OrangeCommon",
					"OrangeSlovakia"					=> "OrangeCommon",
					"OrangeSpain"						=> "OrangeCommon",
					"OrangeCommon"						=> "EUCommon"
			);
			

eval
{
	validateArguments(); #any validation check for the arguments
	setupEnvironment(); #any setup in terms of the environment
	if ($QGP_pack eq 'Default'){
		getDefaultValue();
	}
	else{
		executeTest(); #execute logic
	}
	cleanupEnvironment(); #any cleanup if necessary
};



# Function: validateArguments
#
# Validates the arguments of the script
#
# Parameters:
#
# 		None
#
# Returns:
# 		None

sub validateArguments {
		print("I\n");
		if(!$QGP_pack) {
				print("A valid argument was not entered for QGP_pack, setting to 'Default Value'\n");
				$QGP_pack = "Default Value";
		}
		if(!$excelFile) {
				print("A valid argument was not entered for excelFile, setting to 'default'\n");
				my $path = getcwd;
				$excelFile = "$path\\Validation_Sheet_V1.0.xlsx";
		}
		if(!$QGP_pack_type) {
				print("A valid argument was not entered for QGP_pack_type, setting to 'vendor'\n");
				$QGP_pack_type = "vendor";
		}
}


# Function: setupEnvironment
#
# Setup needed before running the tests
#
# Parameters:
#
# 		None
#
# Returns:
# 		None
#
sub setupEnvironment {
		$testCaseName = "QGP_Pack_Validation";
		print("----------------------------------------------------------------------------\n");
		print("QGP Automated Pack Validation: \n");
		print("\n");
}


# Function: executeTest
#
# Runs the test
#
# Parameters:
#
# 		None
#
# Returns:
# 		None
#
sub executeTest {

		print "*****************QGP_pack_type:$QGP_pack_type******************\n";
		
		my ($features, $commands, $values, $testcaseNum) = parseXLSX($excelFile,$QGP_pack,$QGP_pack_type);
		my $subTestComment;
		my $result;
		my $checkValue;
		my $change_value;
		print "TC_ID,Feature,Expected Value, Actual Value, Result\n";
		my @Array_storage = ([ "ID", "Feature","Expected Value","Actual Value","Result","Comments"],);
		for(my $i = 1; $i <= $testcaseNum; $i++){
				$QGP_pack = $QGP_pack_initial;
				print("----------------------------------------------------------------------------\n");
				print("Test Case $i. @$features[$i].\n");
				print("----------------------------------------------------------------------------\n");

				($result,$checkValue,$change_value) = checkValue(@$values[$i],@$commands[$i],$QGP_pack,$QGP_pack_type);

				if (($result eq 0)){
						
						$passCtr++;
						print("*************** TESTCASE $i PASSED ****************\n");
						print("\n");
						$subResult = 0;
						$subTestComment = "";
						@$values[$i] =~ s/[\n\r]|,/ /g;
						$checkValue=~ s/,/ /g;
						print "$i, @$features[$i], @$values[$i], $checkValue, Pass\n";
						push (@Array_storage, [$i, @$features[$i], @$values[$i], $checkValue, "Pass",$change_value]);
						#push (@Array_storage, [$i, @$features[$i], $expectedVal, $checkValue, "Pass"]);
				}
				elsif(($result eq 1)) {
						
						push (@failedTestcases,", ".$i);
						print("*************** TESTCASE $i FAILED ****************\n");
						print("\n");
						$subResult = 1;
						$subTestComment = "ExpectedValue: ".@$values[$i]." Actual Value: ".$checkValue;
						@$values[$i] =~ s/,/ /g;
						$checkValue=~ s/,/ /g;
						print "$i, @$features[$i], @$values[$i], $checkValue, Failed\n";
						push (@Array_storage, [$i, @$features[$i], @$values[$i], $checkValue, "Failed",$change_value]);
						#push (@Array_storage, [$i, @$features[$i], $expectedVal, $checkValue, "Failed"]);
				}
				elsif(($result eq 2)){
						push (@Array_storage, [$i, @$features[$i], @$values[$i], $checkValue, "Skipped",$change_value]);
				}
				$QGP_pack = $QGP_pack_initial;
		print("*************** TESTCASE $i excel ****************\n");
		
	}
	my $workbook = Spreadsheet::WriteExcel->new("$QGP_pack.xls");
	my $worksheet = $workbook->add_worksheet();
	my $row = 0; 
	foreach my $rslt(@Array_storage)
	{
		$worksheet->write($row, 0, @$rslt[0]);
		$worksheet->write($row, 1, @$rslt[1]);
		$worksheet->write($row, 2, @$rslt[2]);
		$worksheet->write($row, 3, @$rslt[3]);
		$worksheet->write($row, 4, @$rslt[4]); 
		$worksheet->write($row, 5, @$rslt[5]); 
		$row += 1
	}
}


sub parseExcel{
		my $excelFile = shift;
		my $QGP_pack = shift;
		my @features;
		my @commands;
		my $packColumn = 100;
		my $excel = Spreadsheet::XLSX -> new ($excelFile);
		my $sheet = $excel->Worksheet('Sheet1');
		my $testcaseNum = $sheet->{MaxRow};
		foreach my $row ($sheet->{MinRow} .. $testcaseNum) {
				foreach my $col ($sheet->{MinCol} ..  $sheet->{MaxCol}) {
						my $cell = $sheet -> {Cells} [$row] [$col];
						if ($col == 1) {
								$features[$row] = $cell->{Val};
						}
						if ($col == 2) {
								$commands[$row] = $cell->{Val};
						}
						if ($cell){
								if ($cell->{Val} ne ""){
										if ($cell->{Val} eq $QGP_pack){
												$packColumn = $col;
										}
								}
						}
				}
		}
		
		return (\@features, \@commands, $testcaseNum);

}

# Function: parseXLSX
#
# Checks the android default Prop
# value with expected value given
#
# Parameters:
# 		$excelFile
# 		$QGP_pack
#
# Returns:
# 		@features
# 		@values
#
sub parseXLSX{
		my $excelFile = shift;
		my $QGP_pack = shift;
		my $QGP_pack_type = shift;
		my @features;
		my @commands;
		my $value;
		my @values;
		my $excel = Spreadsheet::ParseExcel -> new ();
		my $workbook = $excel ->Parse('Baseline.xlsx');
		my $sheet = $workbook->Worksheet('Sheet1');
		my $testcaseNum = $sheet->{MaxRow};
		foreach my $row ($sheet->{MinRow} .. $testcaseNum) {
				foreach my $col ($sheet->{MinCol} ..  $sheet->{MaxCol}) {
						my $cell = $sheet -> {Cells} [$row] [$col];
						if ($col == 1) {
								$value = $cell->{Val}; #delete
								$values[$row] = $value;
						}
				}
		}

		print "******************************\n";
		print "values:@values\n";
		print "******************************\n";


		my $packColumn = 100;
		$excel = Spreadsheet::XLSX -> new ($excelFile);
		$sheet = $excel->Worksheet('Sheet1');
		$testcaseNum = $sheet->{MaxRow};
		foreach my $row ($sheet->{MinRow} .. $testcaseNum) {
				foreach my $col ($sheet->{MinCol} ..  $sheet->{MaxCol}) {
						my $cell = $sheet -> {Cells} [$row] [$col];
						if ($col == 1) {
								$features[$row] = $cell->{Val};
						}
						if ($col == 2) {
								$commands[$row] = $cell->{Val};
						}
						if ($cell){
								if ($cell->{Val} ne ""){
										if ($cell->{Val} eq $QGP_pack){
												$packColumn = $col;
										}
								}
						}
						if ($col == $packColumn) {
								if ($cell){
										$value = $cell->{Val};
										print "******************-------";
										print $value;
										print "-------******************";
										$values[$row] = $value;
								}
						}
				}
		}
		
		return (\@features, \@commands, \@values, $testcaseNum);
}


# Function: checkValue
#
# Compares expected value with
# the actual value given.
#
# Parameters:
# 		$expectedVal
# 		$actualVal
#
# Returns:
# 		$result
#
sub checkValue{
		my $expectedVal = shift;
		my $command = shift;
		my $QGP_pack = shift;
		
		my $QGP_pack_type = shift;
		my $change_value;
		my $command_initial = $command;
		my $count;
		my $actualVal;
		my $result;
		my @expectedVal1_list;
		my $expectedVal1_list;

		if ($QGP_pack ne "Default"){
				($command,$change_value) = changeCommands($command_initial,$QGP_pack,$QGP_pack_type);
				print "After change command for first time:$change_value\n";
				if ($change_value eq "No APK"){
					print "No APK exists in son pack, change to Father pack\n";
					($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"No APK");
					if ($change_value eq "No APK"){
						print "No APK exists in Father pack, change to GrandFather pack\n";
						($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"No APK");
						if($change_value ne "Change to father pack mode"){
							print "No APK exists in son/Father/Grandfather directory, follow baseline\n";
							$change_value = "No APK exists in son/Father/Grandfather directory, follow baseline";
						}
					}
					elsif($change_value eq "No overlay"){
						print "No APK exists in Father pack, change to GrandFather pack\n";
						($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"No overlay");
						if($change_value ne "Change to father pack mode"){
							print "No APK exists in son/Father/Grandfather directory, follow baseline\n";
							$change_value = "No APK exists in son/Father/Grandfather directory, follow baseline";
						}
					}
					else{
						
						print "Change commands successfully to father pack mode\n";
					}
				}

				elsif($change_value eq "No overlay"){
					print "No APK exists in son pack, change to Father pack\n";
					($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"No overlay");
					if ($change_value eq "No APK"){
						print "No APK exists in Father pack, change to GrandFather pack\n";
						($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"No APK");
						if($change_value ne "Change to father pack mode"){
							print "No APK exists in son/Father/Grandfather directory, follow baseline\n";
							$change_value = "No APK exists in son/Father/Grandfather directory, follow baseline";
						}
					}
					elsif($change_value eq "No overlay"){
						print "No APK exists in Father pack, change to GrandFather pack\n";
						($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"No Overlay");
						if($change_value ne "Change to father pack mode"){
							print "No APK exists in son/Father/Grandfather directory, follow baseline\n";
							$change_value = "No APK exists in son/Father/Grandfather directory, follow baseline";
						}
					}
					else{
						print "Change commands successfully to father pack mode\n";
					}
				}

				elsif ($change_value eq "Change successfully"){
					print "Change commands successfully\n";
				}
				elsif ($change_value eq "Default command"){
					print "No Commands change\n";
				}
		}
		
		$actualVal = runCaseCommand($command);

		($expectedVal, $actualVal) = dealResult($expectedVal, $actualVal);

		($result,$actualVal) = compareResult($command, $expectedVal, $actualVal);


		if ( ($actualVal eq "") && ($change_value eq "Change successfully") ){
				print "Return nothing after change commands, need to change to father pack\n";
				($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"Change successfully");
				if($change_value eq "Change to father pack mode"){
					$actualVal = runCaseCommand($command);
					($expectedVal, $actualVal) = dealResult($expectedVal, $actualVal);
					if ($actualVal eq ""){
						print "Return nothing after change to Fatherpack, need to change to GrandFather pack\n";	
						($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"Change to father pack mode");
						$change_value = "No return value by parsing APK/Father APK";
						
						$actualVal = runCaseCommand($command);
						($expectedVal, $actualVal) = dealResult($expectedVal, $actualVal);
						if ($actualVal eq ""){
							print "Return nothing after change to GrandFatherpack, follow baseline\n";
							$actualVal = runCaseCommand($command_initial);  #No config in son/father/grandfather APK, back to default cmd
							$change_value = "No return value by parsing APK/Father/grandfather APK, follow baseline";
							($expectedVal, $actualVal) = dealResult($expectedVal, $actualVal);
							($result,$actualVal) = compareResult($command_initial, $expectedVal, $actualVal);
						}
						else{
							$change_value = "Actual value follows GrandFatherpack's value";
							$result = 0;
						}				
						
					}
					else{
						print "Actual value follows Fatherpack's value";
						$change_value = "Actual value follows Fatherpack's value";
						$result = 0;
					}	
				}
				else{
					$actualVal = runCaseCommand($command_initial);  #No config in son/father/grandfather APK, back to default cmd
					$change_value = "No return value by parsing APK and has no father pack, follow baseline";
					($expectedVal, $actualVal) = dealResult($expectedVal, $actualVal);
					($result,$actualVal) = compareResult($command_initial, $expectedVal, $actualVal);	
				}																	
		}
		

		if(($actualVal eq "") && ($change_value eq "Change to father pack mode") ){
			($command,$change_value,$QGP_pack) = checkFatherPack($QGP_pack,$change_value,$command_initial,$QGP_pack_type,"Change to father pack mode");
			$change_value = "No APK exists, and return none from Father APK";
			print "Change to Grand-father mode\n";
			$actualVal = runCaseCommand($command);
			($expectedVal, $actualVal) = dealResult($expectedVal, $actualVal);
			if ($actualVal eq ""){
				$actualVal = runCaseCommand($command_initial);  #No config in son/father/grandfather APK, back to default cmd
				$change_value = "No return value by parsing APK/Father/grandfather APK, follow baseline";
				($expectedVal, $actualVal) = dealResult($expectedVal, $actualVal);
				($result,$actualVal) = compareResult($command_initial, $expectedVal, $actualVal);
			}
			else{
				$change_value = "Actual value follows GrandFatherpack's value";
				$result = 0;
			}	
		}

		if (($actualVal =~ m/.ogg/) &&($result==1)){
				$actualVal =~ s/\s//g;
				$expectedVal =~ s/\s//g;
				my @actualVal = split(/.ogg/, $actualVal);
				my $len1=@actualVal;
				$result =0;
				if($len1>1){
					for (my $i=0;$i<$len1;$i++){
						if($expectedVal =~ m/$actualVal[$i]/){
							print "";
						}
						else{
							$result =1;
							last;
						}
					}
				}
		}

		if (($actualVal eq "string8 \"10\"          string8 \"[10 one]\"") || ($actualVal eq "string8 \"\"")  || ($actualVal eq "string8 \"Scan\"") || ($actualVal eq "ls: /system/media/*.wav: No such file or directory")){
				$result = 0;
		}

		print("Expected Value: $expectedVal\n");
		print("Actual Value:   $actualVal\n");
		return $result, $actualVal,$change_value;
}


# Function: cleanupEnvironment
#
# Remove or clean anything unwanted
#
# Parameters:
#
# 		None
#
# Returns:
# 		None
#
sub cleanupEnvironment {
		system("rm *.apk");
		system("rm dump.txt");
}


# Function: changePath
#
# Change package path in Excel
#
# Parameters:
# 
# 		$commands
#       $QGP_pack
#
# Returns:
# 
# 		$commands
#       $change_value
#
sub changeCommands{
		my $commands = shift;
		$QGP_pack = shift;
		$QGP_pack_type = shift;
		my $Res = 'Res';
		my @command_list;
		my $command_list;
		# all apk name in /overlay/
		my $apkList;
		my $apk;
		my $change_value = "Default command";
		if($commands =~ m/SWEBrowser/){
				$commands =~ s/SWEBrowser/Browser/g;
		}
		if ($commands =~ m/^adb pull/ and $commands =~ m/aapt/ and $commands =~ m/grep/ and $commands =~ m/system\/priv-app/){
					$apkList = `adb shell ls /$QGP_pack_type/$QGP_pack/system/vendor/overlay/`;
					@command_list = split(/system\/priv-app\//,$commands);
					@command_list = split(/\//,$command_list[1]);
					$command_list = "$QGP_pack$command_list[0]$Res";
					# ake name
					#print "******apk command:adb shell ls /$QGP_pack_type/$QGP_pack/system/vendor/overlay/$command_list*********\n";
					$apk = `adb shell ls /$QGP_pack_type/$QGP_pack/system/vendor/overlay/$command_list`;
					#print "*****apk:$apk*****\n";
					#print "*************************\n";
					#print $command_list[0];
					#print "*************************\n";
					#print "apklist:\n";
					#print "$apkList\n";
					if ($apkList =~ m/$command_list[0]/){
							$change_value = "Change successfully";
							if($apk =~ m/.link/){
									$commands =~ s/system\/priv-app/system\/$QGP_pack_type\/overlay/;
									print "************exist apk.link,trace the link********************";
									$commands =~ s/$command_list[0]/$command_list/g;
									#print "********************************\n";
									#print "************************---------\n";
									#print $commands;
									#print "---------***********************\n";
							}
							else{
									if($apk =~ m/.apk/){
											print "************exist apk********************\n";
											$commands =~ s/system\/priv-app/$QGP_pack_type\/$QGP_pack\/system\/vendor\/overlay/;
											$commands =~ s/$command_list[0]/$command_list/g;
											#print "************************---------\n";
											#print $commands;
											#print "---------***********************\n";
										}
									else {
											$change_value = "No APK";
									}
							}
					}		
					else{
							$change_value =	"No overlay";
					}
		}
		elsif($commands =~ m/^adb pull/ and $commands =~ m/aapt/ and $commands =~ m/grep/ and $commands =~ m/system\/framework/){
				my $framework_res = "FrameworksRes";
				my $framework_res_apk = "framework-res";
				$apkList = `adb shell ls /$QGP_pack_type/$QGP_pack/system/vendor/overlay/`;
				$apk = `adb shell ls /$QGP_pack_type/$QGP_pack/system/vendor/overlay/$QGP_pack$framework_res`;
				#print "apklist:\n";
				#print $apkList;
				if ($apkList =~ m/$QGP_pack$framework_res/){
						$change_value = "Change successfully";
						if($apk =~ m/.apk.link/){
											$commands =~ s/system\/framework/system\/$QGP_pack_type\/overlay\/$QGP_pack$framework_res/;
											print "************exist apk.link, trace the link********************\n";
											$commands =~ s/$framework_res_apk/$QGP_pack$framework_res/g;
											#print "********************************\n";
											#print "************************---------\n";
											#rint $commands;
											#print "---------***********************\n";
									}
						else{
											if($apk =~ m/.apk/){
													print "************exist apk********************\n";
													$commands =~ s/system\/framework/$QGP_pack_type\/$QGP_pack\/system\/vendor\/overlay\/$QGP_pack$framework_res/;
													$commands =~ s/$framework_res_apk/$QGP_pack$framework_res/g;
													#print "************************---------\n";
													#print $commands;
													#print "---------***********************\n";
												}
											else {
													$change_value = "No APK";
											}
									}
				}
				else{
							$change_value =	"No overlay";
					}

		}

		elsif ($commands =~ m/^adb pull/ and $commands =~ m/aapt/ and $commands =~ m/grep/ and $commands =~ m/system\/app/){
					$apkList = `adb shell ls /$QGP_pack_type/$QGP_pack/system/vendor/overlay/`;
					@command_list = split(/system\/app\//,$commands);
					@command_list = split(/\//,$command_list[1]);
					$command_list = "$QGP_pack$command_list[0]$Res";
					# ake name
					$apk = `adb shell ls /$QGP_pack_type/$QGP_pack/system/vendor/overlay/$command_list`;
					#print "*************************\n";
					#print $command_list[0];
					#print "*************************\n";
					if ($apkList =~ m/$command_list[0]/){
							$change_value = "Change successfully";
							if($apk =~ m/.apk.link/){
									$commands =~ s/system\/app/system\/$QGP_pack_type\/overlay/;
									print "************exist apk.link, trace the link******************\n";
									$commands =~ s/$command_list[0]/$command_list/g;
									#print "********************************\n";
									#print "************************---------\n";
									#print $commands;
									#print "---------***********************\n";
							}
							else{
									if($apk =~ m/.apk/){
											print "************exist apk********************\n";
											$commands =~ s/system\/app/$QGP_pack_type\/$QGP_pack\/system\/vendor\/overlay/;
											$commands =~ s/$command_list[0]/$command_list/g;
											#print "************************---------\n";
											#print $commands;
											#print "---------***********************\n";
										}
									else {
											$change_value = "No APK";
									}
							}
					}
					else{
							$change_value =	"No overlay";
					}
		}
		
		return $commands,$change_value;
}


# Function: checkFatherPack
#
# Change to father package path
#
# Parameters:
# 
# 		$QGP_pack
#       $change_value
#		$command
#		$QGP_pack_type
#		$Comment
#
# Returns:
# 
# 		$command
#       $change_value
#
sub checkFatherPack{
		our $QGP_pack = shift;
		my $change_value = shift;
		my $command = shift;
		my $QGP_pack_type = shift;
		my $Comment = shift;

		print "Before change pack: $QGP_pack\n";
		if(exists $Father_Pack{$QGP_pack}){
			$QGP_pack = $Father_Pack{$QGP_pack};
			print "After change pack: $QGP_pack\n";
			($command,$change_value) = changeCommands($command,$QGP_pack,$QGP_pack_type);
			if ($change_value eq "Change successfully"){
				$change_value = "Change to father pack mode";
				print "change father pack successfully\n";
				#print "After change father pack, command:\n";
				#print "$command\n";
			}
			#print "$command\n";
		}
		else{
			print "No father pack\n";
		}
		return $command,$change_value,$QGP_pack;
}


# Function: runCaseCommand
#
# Run test case command
#
# Parameters:
# 
#		$command
#
# Returns:
# 
# 		$actualVal
#
sub runCaseCommand{
		my $command = shift;

		my $actualVal;
		my $result = 1;
		my @commands = split("\n",$command);
		my $apk = substr $commands[0], -10;
		$apk =~ s/[\n\r]| //g;
		my $ls = (`ls`);
		$ls =~ s/[\n\r]/ /g;

		#Run Commands to get the Actual Value output from device
		for (my $i=0; $i< scalar(@commands); $i++){
				if($commands[$i] =~ m/adb pull/){
						if($ls =~ m/$apk/){
								print("INFORMATIONAL, adb pull skipped\n");
						}
						else {
								#print ("$commands[$i]");
								system("$commands[$i]");
						}
				}
				else {
						#print ("$commands[$i]");
						$actualVal = (`$commands[$i]`);
				}
				sleep(1);
		}
		return $actualVal;
}


# Function: dealResult
#
# Modify expected value and actual value
#
# Parameters:
# 
#		$expectedVal
#		$actualVal
#
# Returns:
# 
# 		$expectedVal
#		$actualVal
#
sub dealResult{
		my $expectedVal = shift;
		my $actualVal = shift;

		#print "before expectedVal:";
		#print "$expectedVal\n";
		#print "before actualVal:";
		#print "$actualVal\n";

		$expectedVal =~ s/\n//g;
		$expectedVal =~ s/^\s*//;
		$expectedVal =~ s/\s*$//;
		$expectedVal =~ s/[\(\)]//g;
		Encode::_utf8_on($expectedVal);
		# $expectedVal =~ s/[\n\r]/\s/g;
		$actualVal =~ s/\n//g;
		$actualVal =~ s/^\s*//;
		$actualVal =~ s/\s*$//;
		$actualVal =~ s/[\(\)]//g;
		Encode::_utf8_on($actualVal);
		# $actualVal =~ s/[\n\r]/\s/g;
		if ($actualVal =~ m/Row: 0/){
			my @actualVal_list = split(/value=/,$actualVal);
			$actualVal = $actualVal_list[1];
		}
		#print "after expectedVal:";
		#print "$expectedVal\n";
		#print "after actualVal:";
		#print "$actualVal\n";

		
		my $d = "d=";
		if($actualVal =~ m/^resource/){
				my @actualVal_list = split(/d=/,$actualVal);
				$actualVal = substr($actualVal_list[1],0,10);
				$actualVal = "$d$actualVal";
		}
		if($expectedVal =~ m/^resource/){
				my @expectedVal_list = split(/d=/,$expectedVal);
				$expectedVal = substr($expectedVal_list[1],0,10);
				$expectedVal = "$d$expectedVal";

		}

		#if (("(string8)" =~ m/$expectedVal/) && ("(string8)" =~ m/$actualVal/)){
			#$expectedVal =~ s/[\(\)]//g;
			#$actualVal =~ s/[\(\)]//g;
			
		#}

	

		if (($expectedVal eq "") && ($actualVal eq "")){
			$expectedVal= " ";
			$actualVal= " ";
			
		}
		print("Actual Value:   $actualVal\n");
		return $expectedVal, $actualVal;
}


# Function: compareResult
#
# Compare result
#
# Parameters:
# 
#		$command
#		$expectedVal
#		$actualVal
#
# Returns:
# 
# 		$result
#		$actualVal
#
sub compareResult{
		my $command = shift;
		my $expectedVal = shift;
		my $actualVal = shift;
		my $result = 1;
		if(($command =~ m/adb pull/) || ($command =~ m/adb shell ls/) || ($command =~ m/adb shell cat/) || ($command =~ m/adb shell dumpsys/) || ($command =~ m/adb shell content/)){
				#print "expectedVal:";
				#print "$expectedVal\n";
				#print "actualVal:";
				#print "$actualVal\n";
				if(($command =~ m/supported_locales/) || ($command =~ m/preferred_network_mode_values/)){
					my @expectedVal1_list = split(/\,/,$expectedVal);
					#print "expectedVal1_list:\n";
					#print @expectedVal1_list;
					my $len1=@expectedVal1_list;
					for(my $i =0; $i<$len1; $i++){
						if($actualVal=~ m/$expectedVal1_list[$i]/){
							print $expectedVal1_list[$i];
							
						}
						else{
							print "Fail: $expectedVal1_list[$i]";
							$result = 1;
							last;
						}
					}
					$result = 0;
				}
				elsif($actualVal =~ m/$expectedVal/){
						$actualVal = $expectedVal;
						$actualVal =~ s/[\n\r]/ /g;
						$result = 0;
				}
				
				#elsif($expectedVal =~ m/$actualVal/){
				#		$expectedVal = $actualVal;
				#		$expectedVal =~ s/[\n\r]/ /g;
				#		$result = 0;
				#}
			}
		elsif($command =~ m/apns-conf.xml/){
					if($actualVal =~ m/$expectedVal/){
						$actualVal = $expectedVal;
						$actualVal =~ s/[\n\r]/ /g;
						$result = 0;
					}
					else{
					$actualVal = "APN not found.";
					}
				$expectedVal =~ s/[\n\r]//g;
				print("\n");
				print("Expected Value: $expectedVal\n");
				print("Actual Value: $actualVal\n");
				print("\n");
			}
		elsif( ($command  =~ m/adb shell getprop/) || ($command =~ m/adb shell settings get/)){
				$actualVal =~ s/[\n\r]| //g;
				$expectedVal =~ s/[\n\r]| //g;
				if($actualVal eq $expectedVal){
						$result = 0;
				}
				print("\n");
				print("Expected Value: $expectedVal\n");
				print("Actual Value:   $actualVal\n");
				print("\n");
		}

		
		else{
				print("\n");
				print("Invalid Command: $command\n");
				print("\n");
				$result = 1;
		}
		return $result, $actualVal;
}


sub getDefaultValue{
		my ($features, $commands, $testcaseNum) = parseExcel($excelFile,$QGP_pack);
		print "testcaseNum:$testcaseNum\n";
		my @default_value;
		for(my $i = 1; $i <= $testcaseNum; $i++){
				print("----------------------------------------------------------------------------\n");
				print("Get default value. Test $i case.\n");
				print("----------------------------------------------------------------------------\n");
				my $actualVal = runCaseCommand(@$commands[$i]);
				print $actualVal;
				push(@default_value, $actualVal);
		}
		my $workbook = Spreadsheet::WriteExcel->new('Baseline.xlsx');
		my $worksheet = $workbook->add_worksheet();
		for(my $i = 1; $i <= $testcaseNum; $i++){
				$worksheet->write(0, 0, 'ID'); 
				$worksheet->write(0, 1, 'Default Vaule'); 
				$worksheet->write($i, 0, $i); 
				$worksheet->write($i, 1, $default_value[$i-1]); 
		}
}


exit 0;
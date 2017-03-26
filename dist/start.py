# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-03-25 15:23:07
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-03-25 18:57:46

import googleAuth
import logicHandler
import datetime
import os

def main():
	newDocTitle = "Survey Assignments " + datetime.date.strftime(datetime.date.today(), '%d%B%Y')

	agents = logicHandler.getAgents()
	surveysFile = logicHandler.getNewestFile()
	surveysFile = logicHandler.trimDataAndGroup(surveysFile)

	totalSRs, totalOldSRs = logicHandler.collectEmailStats(surveysFile)

	surveysFile, agents = logicHandler.assignSurveys(surveysFile, agents)
	csvFile = logicHandler.combine_to_csv(surveysFile, agents)

	sheetService = googleAuth.getSheetService()
	newSpreadsheet = googleAuth.addSpreadsheet(sheetService, title=newDocTitle)
	result_of_adding = googleAuth.add_lines_to_spreadsheet(sheetService, newSpreadsheet['spreadsheetId'], csvFile)
	result_of_sharing = googleAuth.shareDocument(newSpreadsheet['spreadsheetId']).execute()
	sheetURL = newSpreadsheet['spreadsheetUrl']

	emailBody = logicHandler.getEmail(totalSRs, totalOldSRs, sheetURL)

	print (emailBody)
	emailFilename = datetime.date.strftime(datetime.date.today(), '%d%B%Y') + "SurveyEmail.txt"
	emailFilePath = os.path.join(logicHandler.vixxoUploadDirectory, emailFilename)
	with open(emailFilePath, 'w') as outfile:
		outfile.write(emailBody)

if __name__ == '__main__':
	main()